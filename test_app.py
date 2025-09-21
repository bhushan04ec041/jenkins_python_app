# test_app.py
import pytest
from unittest.mock import patch, MagicMock

# Mock psycopg2 before importing app
mock_conn = MagicMock()
mock_cursor = MagicMock()
# Predefined data for GET requests
mock_cursor.fetchall.return_value = [(101, "John"), (102, "Alice")]
mock_conn.cursor.return_value = mock_cursor

with patch("psycopg2.connect", return_value=mock_conn):
    from app import app  # import app after mocking

# Mock Redis to avoid connection issues
mock_redis = MagicMock()
with patch("app.redis", mock_redis):

    # Flask test client fixture
    @pytest.fixture
    def client():
        with app.test_client() as client:
            yield client

    # Test GET request to '/'
    def test_index_get(client):
        """Test GET request returns 200 and page content"""
        response = client.get("/")
        assert response.status_code == 200
        # Check that some text from the page is present
        assert b"Submitted Employees" in response.data
        # Check that mocked employees are displayed
        assert b"John" in response.data
        assert b"Alice" in response.data

    # Test POST request to '/' with sample data
    def test_index_post(client):
        """Test POST request adds new employee"""
        response = client.post("/", data={"id": 103, "name": "Bob"})
        assert response.status_code == 200
        # Check that POSTed employee appears in page
        assert b"Bob" in response.data
        # Verify Redis was called
        mock_redis.rpush.assert_called_with('employees', '103:Bob')
        # Verify SQL INSERT executed
        mock_cursor.execute.assert_called()