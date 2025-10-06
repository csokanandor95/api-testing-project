import pytest
from api_requests import (
    get_popular_movies,
    get_movie_details,
    search_movie,
)

# pozitív tesztek

def test_tc01_popular_movies():
    """TC01: Népszerű filmek lekérdezése"""
    response = get_popular_movies()
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert len(data["results"]) > 0

def test_tc02_movie_details_valid_id():
    """TC02: Film részletek érvényes ID-vel (Inception - 27205)"""
    response = get_movie_details(27205)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 27205
    assert "title" in data
    assert "overview" in data

def test_tc03_search_movie_valid_query():
    """TC03: Film keresés érvényes kifejezéssel (The Naked Gun)"""
    response = search_movie("The Naked Gun")
    assert response.status_code == 200
    data = response.json()
    assert len(data["results"]) > 0