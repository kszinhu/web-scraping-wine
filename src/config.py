import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(verbose=True)
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Get secret key from environment variable .env
SECRET_KEY = os.environ.get('API_SECRET_KEY')
API_TOKEN = os.environ.get('API_TOKEN')
SCRAPING_URL = os.environ.get('SCRAPING_URL')
DEBUG = os.environ.get('DEBUG') != None or False

# Add config to config object
config = {
  'DEBUG': DEBUG,
  'SCRAPING_URL': SCRAPING_URL,
  'SECRET_KEY': SECRET_KEY,
  'API_TOKEN': API_TOKEN
}
  