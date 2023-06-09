import os
import tempfile
import json
import pytest
from backend import create_app
from backend.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def register(self):
        payload = {
            'username': 'guitarhero',
            'password': 'jimihen'
        }

        json_payload = json.dumps(payload)
        self._client.post('/auth/register', data = json_payload.encode('utf8'), content_type = 'application/json')

    def login(self):
        payload = {
        'username': 'guitarhero',
        'password': 'jimihen'
        }

        json_payload = json.dumps(payload)
        return self._client.post('auth/login', data = json_payload.encode('utf8'), content_type = 'application/json')
    
@pytest.fixture
def auth(client):
    return AuthActions(client)
