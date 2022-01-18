import pytest
from src import app as server

@pytest.fixture
def client():
    server.app.config['TESTING'] = True
    client = server.app.test_client()
    yield client