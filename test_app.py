import pytest
import psycopg2
from app import app

# PostgreSQL connection details (match your app.py)
DB_HOST = "postgres"
DB_NAME = "mydatabase"
DB_USER = "myuser"
DB_PASSWORD = "mypassword"

@pytest.fixture(scope="module")
def test_client():
    # Flask provides a test client for requests
    with app.test_client() as client:
        yield client

@pytest.fixture(scope="module")
def db_cursor():
    # Connect to the actual PostgreSQL database
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()
    # Ensure the table exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS empdata (
            id INT PRIMARY KEY,
            name VARCHAR(255)
        );
    """)
    conn.commit()
    yield cursor
    # Clean up test data
    cursor.execute("DELETE FROM empdata;")
    conn.commit()
    cursor.close()
    conn.close()

def test_index_get(test_client):
    """Test GET request to /"""
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"Enter Employee Data for profinch" in response.data

def test_index_post(test_client, db_cursor):
    """Test POST request to / and DB insertion"""
    # Send POST data
    response = test_client.post('/', data={'id': 101, 'name': 'John Doe'})
    assert response.status_code == 200

    # Verify insertion in PostgreSQL
    db_cursor.execute("SELECT * FROM empdata WHERE id = 101;")
    result = db_cursor.fetchone()
    assert result == (101, 'John Doe')

def test_redis_push():
    """Test Redis push functionality"""
    from app import redis
    redis.rpush('employees', "999:Jane")
    result = redis.lrange('employees', -1, -1)[0]
    assert result == "999:Jane"
    # Clean up
    redis.lpop('employees')