import re
import time
import sqlalchemy
import tzlocal
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
        print('\n --- Scraping and saving to database')

        # If the wines table wasn't created yet, create it
        if not db.engine.dialect.has_table(db.engine, 'wines'):
            db.create_all()

        # Get the data from the website
        products = get_data()

        # If there are products, save them to the database
        if products:
            for product in products:
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
                        print('\n :( Wine already exists')
                    else:
                        raise e
                except sqlalchemy.exc.InvalidRequestError as e:
                    if 'This Session\'s transaction has been rolled back' in str(e):
                        print('\n :( Wine already exists')

                except Exception as e:
                    continue
                
        else:
            raise Exception('No products found')

        if db.session.query(WineModel).count() > 0:
            print('Products saved:', db.session.query(WineModel).count())

        print('\n --- Data saved to database')


scheduler = BackgroundScheduler(timezone=str(tzlocal.get_localzone()))

if __name__ == '__main__':
    try:
        # (Test) Run the function every 5 seconds
        # (Production) Run the function every day (24 hours)
        scheduler.add_job(scrape_and_save, 'interval', seconds=5)
        # scheduler.add_job(scrape_and_save, 'interval', hours=24)

        scheduler.start()
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print('\n --- Stopped scraping')
        print('\n --- Exiting')
        exit()
    except sqlalchemy.exc.InvalidRequestError as e:
        db.session.rollback()
        print('\n --- Exiting')
        exit()
    finally:
        db.session.close()
        print('\n --- Exiting')
