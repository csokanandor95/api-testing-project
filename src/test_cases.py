import pytest
from api_requests import (
    get_popular_movies, 
    
)

# pozitív tesztek

def test_tc01_popular_movies():
    """TC01: Népszerű filmek lekérdezése"""
    response = get_popular_movies()
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert len(data["results"]) > 0