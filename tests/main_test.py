"""
Unit tests for Flask app
"""
from app.main import CFG_PORT

def test_port() -> None:
    """
    Tests the setup of the API endpoint
    """
    assert CFG_PORT == 5000
