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
SQLALCHEMY_DATABASE_URI = f"sqlite:///src/server/{DB_NAME}.db"


def db_prep():
    print("\n Preparing database...")
    if not database_exists(SQLALCHEMY_DATABASE_URI):
        create_database(SQLALCHEMY_DATABASE_URI)
    print("\n Database prepared!")

def apply_config(application):
    application.config['TESTING'] = True
    application.config['API_TOKEN'] = os.getenv('API_TOKEN')
    application.config['DEBUG'] = True
    
@pytest.fixture(scope="session")
def faker_seed():
    return 774577

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
                link=f"{fake.unique.url()}{i}"
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
        print("\n Dropping database...")
        db.session.remove()
        db.drop_all()
