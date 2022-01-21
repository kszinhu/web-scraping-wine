import re
import time
from apscheduler.schedulers.background import BackgroundScheduler
from requests import get
from bs4 import BeautifulSoup
from ..db import db
from ..app import app

def get_data():
    response = get('https://www.amazon.com.br/s?k=vinho')
    soup = BeautifulSoup(response.text, 'lxml')

    # Get all the products
    products = soup.find_all(
        'div', attrs={'data-component-type': 's-search-result'})

    keys = { 
    'name': { 
        'element': 'span',
        'attrs': {
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
            product_dict

def scrape_and_save():
    with app.app_context():
        # Get data from Amazon
        products = get_data()
        # Save data to database
        if products:
            for product in products:
                product_db = db.Product(
                    name=product['name'],
                    price=product['price'],
                    image=product['image'],
                    link=product['link']
                )
                db.session.add(product_db)
        db.session.commit()
        print('\n --- Data saved to database')

# (Test) Run the function every 5 seconds
scheduler = BackgroundScheduler()
# (Production) Run the function every day at 00:00 (TZ = Brasilia)
# schedule.every().day.at("00:00").do(get_data)

if __name__ == '__main__':
    scheduler.add_job(scrape_and_save, 'interval', seconds=5)
    scheduler.start()
    while True:
        time.sleep(1)