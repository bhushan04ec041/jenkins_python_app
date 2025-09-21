# test_app.py
import pytest
from unittest.mock import patch, MagicMock

# Patch psycopg2.connect globally before importing app
mock_conn = MagicMock()
mock_cursor = MagicMock()
mock_cursor.fetchall.return_value = [(101, "John"), (102, "Alice")]
mock_conn.cursor.return_value = mock_cursor

with patch("psycopg2.connect", return_value=mock_conn):
    from app import app  # import after patching

# Flask test client
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_index_get(client):
    """Test GET request returns 200"""
    rv = client.get("/")
    assert rv.status_code == 200
    assert b"Submitted Employees" in rv.data

def test_index_post(client):
    """Test POST request adds employee"""
    rv = client.post("/", data={"id": 103, "name": "Bob"})
    assert rv.status_code == 200
    assert b"Bob" in rv.data