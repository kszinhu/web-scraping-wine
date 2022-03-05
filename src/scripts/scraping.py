import re
import sqlalchemy
import tzlocal
import time
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from requests import get
from bs4 import BeautifulSoup
from ..db import db
from ..app import app
from ..config import config
from ..models.wine import WineModel


def get_data():

    for id in range(25700, 25750):
        url = f'https://www.wine.com.br/api/v2/products/{id}?expand=attributes'
        response = get(url)

        soup = BeautifulSoup(response.text, 'lxml')

        type = soup.find('type')
        available = soup.find('available')
        
        if type is not None and available is not None and available.text == 'true' and type.text == 'Vinho':
            product = {
                'name': soup.find('name').text,
                'price': soup.find('listprice').text,
                'year': soup.find('year').text,
                'country': soup.find('attributes').find('country').text,
                'type': soup.find('attributes').find('type').text,
                'image': f'https://www.wine.com.br/cdn-cgi/image/f=png,h=515,q=99/assets-images/produtos/{id}-01.png',
            }
            print(product)
            yield product


def scrape_and_save():
    with app.app_context():
        print('\n --- Scraping and saving to database\n')

        # If the wines table wasn't created yet, create it
        if not db.engine.dialect.has_table(db.engine, 'wines'):
            db.create_all()

        # Get the data from the website
        products = get_data()

        # If there are products, save them to the database
        if products:
            for index, product in enumerate(products):
                try:
                    wine = WineModel(
                        name=product['name'],
                        price=product['price'],
                        year=product['year'],
                        country=product['country'],
                        type=product['type'],
                        image=product['image'],
                    )
                    wine.save_to_db()

                except sqlalchemy.exc.IntegrityError as e:
                    if 'UNIQUE constraint failed' in str(e):
                        print(f"\t :( {product['name']} already exists")

                except sqlalchemy.exc.InvalidRequestError as e:
                    print(f"\t :( {product['name']} already exists")

                except Exception as e:
                    pass

        else:
            raise Exception('\n :( No products found')

        try:
            db.session.rollback()
            if db.session.query(WineModel).count() > 0:
                print('\n\t Products saved:',
                      db.session.query(WineModel).count())
        except sqlalchemy.exc.InvalidRequestError as e:
            pass

        print('\n --- Data saved to database')


scheduler = BackgroundScheduler(timezone=str(tzlocal.get_localzone()))

if __name__ == '__main__':
    try:
        if config['ENVIRONMENT'] == 'development':
            # (Development) Run the job immediately and then every 30 seconds
            try:
                scheduler.add_job(scrape_and_save, 'interval',
                                  seconds=30, next_run_time=datetime.now())
            except Exception:
                pass

        elif config['ENVIRONMENT'] == 'production':
            # (Production) Run the job immediately and then every day
            try:
                scheduler.add_job(scrape_and_save, 'interval',
                                  days=1, next_run_time=datetime.now())
            except Exception:
                pass

        scheduler.start()

        while True:
            time.sleep(1)

    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print('\n --- Stopped scraping')
        print('\n --- Exiting')

    except sqlalchemy.exc.InvalidRequestError as e:
        db.session.rollback()
        print('\n --- Exiting')

    finally:
        db.session.close()
        print('\n --- Exiting')
