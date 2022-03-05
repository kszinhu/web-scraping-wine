from distutils.log import debug
import os
import pytest
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.exc import OperationalError, ProgrammingError
from sqlalchemy_utils import database_exists, create_database
from src.app import server as application

load_dotenv()

DB_NAME = f"{os.getenv('DB_NAME')}_test"
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASSWORD')
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

def db_prep():
    # Preparing database
    if not database_exists(SQLALCHEMY_DATABASE_URI):
        create_database(SQLALCHEMY_DATABASE_URI)


def apply_config(application):
    application.config['TESTING'] = True
    application.config['API_TOKEN'] = os.getenv('API_TOKEN')
    application.config['DEBUG'] = True


@pytest.fixture(scope="session")
def faker_seed():
    return 774577


@pytest.fixture
def procfile_command():
    # get the commands from the procfile and return them as a list
    with open('Procfile') as f:
        commands = f.read().splitlines()
    return commands


@pytest.fixture(scope="session", autouse=True)
def client_no_headers():
    # Prepare database (create if not exists and drop if exists)
    db_prep()

    # Use Faker to generate fake data
    from faker import Faker
    fake = Faker()

    # generate fake data for all models using sqlalchemy
    from src.models import wine

    # Create fake data for WineModel
    wine_data = []
    for i in range(10):
        wine_data.append(
            wine.WineModel(
                name=fake.name(),
                price=fake.random_int(min=10, max=100),
                image=f"{fake.unique.image_url()}{i}",
                country=fake.country(),
                type='Vinho',
                year=fake.year(),
            )
        )

    # Up to fake data for all models
    from src.db import db

    # Setup application
    apply_config(application.app)

    with application.app.app_context():
        db.create_all()
        db.session.add_all(wine_data)
        db.session.commit()

    # Create a test client
    with application.app.test_client() as client:
        yield client

    # Clean up database
    with application.app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="session", autouse=True)
def client():
    # Prepare database (create if not exists and drop if exists)
    db_prep()

    # Use Faker to generate fake data
    from faker import Faker
    fake = Faker()

    # generate fake data for all models using sqlalchemy
    from src.models import wine

    # Create fake data for WineModel
    wine_data = []
    for i in range(10):
        wine_data.append(
            wine.WineModel(
                name=fake.name(),
                price=fake.random_int(min=10, max=100),
                image=f"{fake.unique.image_url()}{i}",
                year=fake.random_int(min=1900, max=2022),
                country=fake.country(),
                type='Vinho',
            )
        )

    # Up to fake data for all models
    from src.db import db

    # Setup application
    apply_config(application.app)

    with application.app.app_context():
        db.create_all()
        db.session.add_all(wine_data)
        db.session.commit()

    # Create a test client
    with application.app.test_client() as client:
        token = client.application.config['API_TOKEN']
        # Add header to all requests to simulate an API call
        client.environ_base['HTTP_WINE_TOKEN'] = token
        yield client

    # Clean up database
    with application.app.app_context():
        db.session.remove()
        db.drop_all()
