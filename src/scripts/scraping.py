from requests import get
from bs4 import BeautifulSoup
import re

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
        print(product_dict)
