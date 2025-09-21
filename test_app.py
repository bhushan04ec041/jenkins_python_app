# test_app.py
import pytest
from unittest.mock import patch, MagicMock

# Mock psycopg2.connect before importing app to avoid connection errors
mock_conn = MagicMock()
mock_cursor = MagicMock()
mock_cursor.fetchall.return_value = [(101, "John Doe"), (102, "Jane Smith")]
mock_conn.cursor.return_value = mock_cursor

# Also mock Redis to avoid connection issues
mock_redis = MagicMock()

# Apply both mocks before importing app
with patch("psycopg2.connect", return_value=mock_conn), \
     patch("app.Redis", return_value=mock_redis):
    from app import app

# Flask test client fixture
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_get(client):
    """Test GET request to root endpoint returns 200"""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Enter Employee Data for profinch" in response.data
    assert b"Submitted Employees" in response.data

def test_index_post(client):
    """Test POST request to root endpoint returns 200 and processes data"""
    response = client.post("/", data={"id": "103", "name": "Bob"})
    assert response.status_code == 200
    assert b"Bob" in response.data
    
    # Verify Redis was called
    mock_redis.rpush.assert_called_with('employees', '103:Bob')
    
    # Verify database insert was attempted
    mock_cursor.execute.assert_called()

def test_index_post_invalid_data(client):
    """Test POST request with invalid data"""
    response = client.post("/", data={"id": "", "name": ""})
    assert response.status_code == 200  # Should still return 200, just won't process