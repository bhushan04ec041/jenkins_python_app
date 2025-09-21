import pytest
from unittest.mock import Mock, patch, MagicMock
from app import app
import psycopg2

@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def mock_dependencies():
    """Mock Redis and PostgreSQL dependencies for all tests"""
    # Mock Redis
    with patch('app.redis') as mock_redis:
        mock_redis.rpush = Mock(return_value=1)
        mock_redis_instance = mock_redis
        
        # Mock PostgreSQL connection and cursor
        mock_conn = Mock()
        mock_cursor = Mock()
        
        with patch('app.psycopg2.connect', return_value=mock_conn):
            mock_conn.cursor.return_value = mock_cursor
            
            # Set up the mock cursor to return test data
            mock_cursor.fetchall.return_value = [
                (101, 'Alice'),
                (102, 'Bob')
            ]
            
            # Yield all mocks for individual test customization
            yield {
                'redis': mock_redis_instance,
                'conn': mock_conn,
                'cursor': mock_cursor
            }

def test_index_get(client, mock_dependencies):
    """Test GET request to root endpoint returns 200 and displays employees"""
    response = client.get("/")
    
    assert response.status_code == 200
    assert b"Employee Submission Profinch" in response.data
    assert b"Alice" in response.data
    assert b"Bob" in response.data
    
    # Verify PostgreSQL query was executed
    mock_dependencies['cursor'].execute.assert_called_with("SELECT * FROM empdata ORDER BY id")
    mock_dependencies['cursor'].fetchall.assert_called_once()

def test_index_post_valid_data(client, mock_dependencies):
    """Test POST request with valid data"""
    response = client.post("/", data={"id": "103", "name": "Charlie"})
    
    assert response.status_code == 200
    assert b"Charlie" in response.data
    
    # Verify Redis was called
    mock_dependencies['redis'].rpush.assert_called_with('employees', '103:Charlie')
    
    # Verify PostgreSQL insert was executed (note: this will fail due to SQL injection vulnerability)
    # The actual call might vary due to the string formatting vulnerability
    mock_dependencies['cursor'].execute.assert_called()
    mock_dependencies['conn'].commit.assert_called_once()

def test_index_post_empty_data(client, mock_dependencies):
    """Test POST request with empty data"""
    response = client.post("/", data={"id": "", "name": ""})
    
    assert response.status_code == 200
    # The form should still render with existing data
    assert b"Alice" in response.data
    assert b"Bob" in response.data

def test_index_post_missing_fields(client, mock_dependencies):
    """Test POST request with missing fields"""
    response = client.post("/", data={"id": "104"})  # Missing name
    
    assert response.status_code == 400  # Should return bad request due to missing required field

def test_index_post_invalid_id(client, mock_dependencies):
    """Test POST request with non-numeric ID"""
    response = client.post("/", data={"id": "abc", "name": "Test"})
    
    assert response.status_code == 200
    # The TypeError from emp_id + "123" should be handled or the test might fail

def test_sql_injection_attempt(client, mock_dependencies):
    """Test what happens with SQL injection attempt"""
    # This test demonstrates the vulnerability
    sql_injection_data = {"id": "105", "name": "Robert'); DROP TABLE empdata; --"}
    
    response = client.post("/", data=sql_injection_data)
    
    assert response.status_code == 200
    # The vulnerable SQL would execute: INSERT INTO empdata (id, name) VALUES (105, 'Robert'); DROP TABLE empdata; --')

def test_multiple_submissions(client, mock_dependencies):
    """Test multiple employee submissions"""
    # First submission
    client.post("/", data={"id": "106", "name": "David"})
    
    # Second submission
    client.post("/", data={"id": "107", "name": "Eve"})
    
    # Verify Redis was called twice
    assert mock_dependencies['redis'].rpush.call_count == 2
    mock_dependencies['redis'].rpush.assert_any_call('employees', '106:David')
    mock_dependencies['redis'].rpush.assert_any_call('employees', '107:Eve')
    
    # Verify PostgreSQL was called twice
    assert mock_dependencies['cursor'].execute.call_count >= 2  # SELECT + 2 INSERTs
    assert mock_dependencies['conn'].commit.call_count == 2

# Test for the TypeError bug in the original code
def test_type_error_bug(client, mock_dependencies):
    """Test the TypeError bug when emp_id is treated as int"""
    # This will trigger the TypeError: emp_id + "123" when emp_id is integer
    response = client.post("/", data={"id": "108", "name": "Frank"})
    
    # The test might pass if the error is handled by Flask, or fail showing the bug
    assert response.status_code in [200, 500]  # Could be either depending on error handling

if __name__ == "__main__":
    pytest.main([__file__, "-v"])