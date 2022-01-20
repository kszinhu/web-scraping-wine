from distutils.log import debug
import os
import pytest
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.exc import OperationalError, ProgrammingError
from sqlalchemy_utils import database_exists, create_database
from src import app as server

load_dotenv()

DB_NAME = f"{os.getenv('DB_NAME')}_test"
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASSWORD')
SQLALCHEMY_DATABASE_URI = f"sqlite:///src/server/{DB_NAME}.db"


def db_prep():
    print("Preparing database...")
    if not database_exists(SQLALCHEMY_DATABASE_URI):
        create_database(SQLALCHEMY_DATABASE_URI)
    print("Database prepared!")


@pytest.fixture(scope="session", autouse=True)
def fake_db():
    # Create a fake database
    db_prep()
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    from src.db import db
    from src.models.wine import WineModel
    MetaData.create_all(engine)
    print(f"{DB_NAME} ready for testing!")
    try:
        yield db
    finally:
        db.session.close()
        db.drop_all()
        os.remove(f"{DB_NAME}.db")
        print(f"{DB_NAME} dropped!")


@pytest.fixture
def client():
    # Create a test client
    client = server.app.test_client()
    # Return the client
    return client

    # # Create the test client
    # server.app.config['TESTING'] = True
    # client = server.app.test_client()

    # # Return the test client
    # yield client

# @pytest.fixture
# def client():
#     # Create a test client
#     server.app.config['TESTING'] = True
#     client = server.app.test_client()

#     # Set up the database (test database)
#     with client.application.app_context():
#         server.db.create_all()

#     yield client

#     # Teardown the database (test database)
#     with client.application.app_context():
#         server.db.session.remove()
#         server.db.drop_all()
