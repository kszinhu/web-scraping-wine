import os
import requests

def check_existence(url):
    auth = {'wine-token': os.environ.get('TEST_TOKEN')}
    response = requests.get(url, headers=auth)
    return response.status_code


def check_auth():
    auth = {'wine-token': os.environ.get('TEST_TOKEN')}
    response = requests.get('http://localhost:5000/wines', headers=auth)
    return response