import re
import time
from apscheduler.schedulers.background import BackgroundScheduler
from requests import get
from bs4 import BeautifulSoup
from ..db import db
from ..app import app
from ..config import config
from ..models.wine import WineModel

def get_data():
    response = get('https://www.amazon.com.br/s?k=vinho&i=grocery')
    soup = BeautifulSoup(response.text, 'lxml')

    # Get all the products
    products = soup.find_all(
        'div', attrs={'data-component-type': 's-search-result'})

    keys = { 
        'name': { 
            'element': 'span',
            'attrs': {
                # a-size-medium a-color-base a-text-normal
                # a-size-base-plus a-color-base a-text-normal
                'class_': 'a-size-base-plus a-color-base a-text-normal'
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
                        product_dict[key] = int(re.sub(r'[^\d]', '', element.text))
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
    # print(get_data())
    with app.app_context():
        # Get data from Amazon
        products = get_data()
        #  Save data to database using client
        if products:
            for product in products:
                wine = WineModel(
                    name=product['name'],
                    price=product['price'],
                    link=product['link'],
                    image=product['image']
                )
                wine.save_to_db()
        else:
            raise Exception('No products found')
        
        if db.session.query(WineModel).count() > 0:
            print('Scraping and saving to database...')
            print('Products saved:', db.session.query(WineModel).count())
            
        print('\n --- Data saved to database')

scheduler = BackgroundScheduler()

if __name__ == '__main__':
    # (Test) Run the function every 5 seconds
    # (Production) Run the function every day (24 hours)
    scheduler.add_job(scrape_and_save, 'interval', seconds=5)
    # scheduler.add_job(scrape_and_save, 'interval', hours=24)
    scheduler.start()
    while True:
        time.sleep(1)