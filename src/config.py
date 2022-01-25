import re, sys, os
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

# Get environment using command line argument (e.g. 'dev' or 'prod')
def get_env(argv) -> str:
    NUM_ARGS = len(argv)
    COMMAND_LINE_STRING = str(argv)
    if NUM_ARGS > 1:
        # if pytest is running, command line argument is 'python3 -m pytest -W ignore::DeprecationWarning --no-header -s -v'
        # we need capture pytest command line argument to set environment = 'test'
        isPytest = re.search('pytest', COMMAND_LINE_STRING) != None
        if isPytest:
            env = 'test'
        else:
            # if running from command line, command line argument is '[src.scripts.scraping --environment=production]'
            # we need capture command line argument to set environment = 'production'
            arg_environment = re.search(
                'environment=(\w+)', COMMAND_LINE_STRING)
            env = arg_environment.group(1)
            return env


# Add config to config object
config = {
    'DEBUG': DEBUG,
    'SCRAPING_URL': SCRAPING_URL,
    'SECRET_KEY': SECRET_KEY,
    'API_TOKEN': API_TOKEN,
    'ENVIRONMENT': get_env(sys.argv) or 'development'
}

if __name__ == '__main__':
    print(config['ENVIRONMENT'])
