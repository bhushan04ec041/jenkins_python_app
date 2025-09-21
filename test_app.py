import pytest
from unittest.mock import Mock, patch
from flask import Flask

# Create a simple test that doesn't import your app directly
def test_basic_flask_app():
    """Simple test that creates a basic Flask app to verify testing works"""
    test_app = Flask(__name__)
    
    @test_app.route('/')
    def hello():
        return 'Hello, World!'
    
    with test_app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
        assert b'Hello, World!' in response.data

def test_math():
    """Simple math test to verify pytest is working"""
    assert 1 + 1 == 2

def test_string():
    """Simple string test"""
    assert "hello".upper() == "HELLO"