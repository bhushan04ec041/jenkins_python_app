# test_app.py
import pytest
from unittest.mock import patch, MagicMock
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Mock PostgreSQL connection and cursor
@pytest.fixture(autouse=True)
def mock_postgres():
    with patch('app.psycopg2.connect') as mock_connect:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        # Example: fake data returned from SELECT
        mock_cursor.fetchall.return_value = [(101, "John Doe"), (102, "Jane Smith")]
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        yield mock_connect

# Mock Redis
@pytest.fixture(autouse=True)
def mock_redis():
    with patch('app.Redis') as mock_redis_cls:
        mock_redis_instance = MagicMock()
        mock_redis_cls.return_value = mock_redis_instance
        yield mock_redis_instance

def test_get_index(client):
    """Test GET request to '/'"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Submitted Employees" in response.data

def test_post_index(client):
    """Test POST request to '/'"""
    response = client.post('/', data={'id': 103, 'name': 'Alice'})
    assert response.status_code == 200
    # Ensure Redis rpush was called
    app.redis.rpush.assert_called_with('employees', '103:Alice')
    # Ensure cursor.execute was called for insert
    app.cursor.execute.assert_called()
