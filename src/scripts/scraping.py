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

    response = get(config['SCRAPING_URL'])
    soup = BeautifulSoup(response.text, 'lxml')

    # Get all the products
    products = soup.find_all(
        'div', attrs={'data-component-type': 's-search-result'})

    keys = {
        'name': {
            'element': 'span',
            'attrs': {
                'class_': 'a-size-medium a-color-base a-text-normal'
            }
        },
        'price': {
            'element': 'span',
            'attrs': {
                'class_': 'a-offscreen'
            }
        },
        'image': {
            'element': 'img',
            'attrs': {
                'class_': 's-image'
            }
        },
        'link': {
            'element': 'a',
            'attrs': {
                'class_': 'a-link-normal s-no-outline'
            }
        }
    }

    # Each product is a dictionary with the following keys:
    # - name (string)
    # - price (in cents)
    # - image (url to the image)
    # - url (url to buy the product)
    if len(products) > 0:
        for product in products:
            product_dict = {}
            for key in keys:
                element = product.find(**keys[key]['attrs'])
                if element:
                    if key == 'price':
                        # Get the price(remove the 'R$' and ',') and convert to cents
                        product_dict[key] = int(
                            re.sub(r'[^\d]', '', element.text))
                    elif key == 'image':
                        product_dict[key] = element['src']
                    elif key == 'link':
                        product_dict[key] = element['href']
                    else:
                        product_dict[key] = element.text
                else:
                    product_dict[key] = None
            yield product_dict
    else:
        return None


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
                        link=product['link'],
                        image=product['image']
                    )
                    wine.save_to_db()
                except sqlalchemy.exc.IntegrityError as e:
                    if 'UNIQUE constraint failed' in str(e):
                        print(f"\t :( {product['name']} already exists")

                        if index == len(enumerate(products)) - 1:
                            print('\n')

                except sqlalchemy.exc.InvalidRequestError as e:
                    print(f"\t :( {product['name']} already exists")

                    if index == len(enumerate(products)) - 1:
                        print('\n')
                except Exception as e:
                    pass

        else:
            raise Exception('\n :( No products found')

        try:
            db.session.rollback()
            if db.session.query(WineModel).count() > 0:
                print('\t Products saved:', db.session.query(WineModel).count())
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
