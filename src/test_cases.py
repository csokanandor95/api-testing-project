"""
TMDB API Teszt Suite

Ez a fájl tartalmazza az összes API tesztet a TMDB (The Movie Database) API-hoz.

Teszt Struktúra:
- Funkcionális tesztek (TC01-TC06): Pozitív esetek, alap funkciók tesztelése
- Negatív tesztek (TC07-TC12): Hibás bemenetek, hibaüzenetek validálása
- Boundary Value Analysis (TC13-TC16): Határérték tesztelés (page paraméter-re)
- Nem-funkcionális tesztek (TC17-TC20): Teljesítmény és adat-integritás

Összesen: 20 teszt eset
Lefedettség: Funkcionális, negatív, határérték, teljesítmény, adat-validáció
"""

import pytest
from api_requests import (
    get_popular_movies,
    get_movie_details,
    search_movie,
    get_movie_genres,
    get_with_custom_key
)

# --Funkcionális tesztek--
# Pozitív tesztek

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

def test_tc04_get_genres():
    """TC04: Műfajok listájának lekérdezése"""
    response = get_movie_genres()
    assert response.status_code == 200
    data = response.json()
    assert "genres" in data
    for genre in data["genres"]:
        assert "id" in genre
        assert "name" in genre

def test_tc05_popular_movies_page_2():
    """TC05: Népszerű filmek 2. oldal"""
    response = get_popular_movies(page=2)
    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 2
    assert len(data["results"]) > 0

def test_tc06_language_parameter():
    """TC06: Magyar nyelvi paraméter"""
    response = get_popular_movies(language="hu-HU")
    assert response.status_code == 200

# --Negatív tesztek--
# Hitelesítési hibák

def test_tc07_invalid_api_key():
    """TC07: Hibás API kulcs"""
    response = get_with_custom_key("movie/popular", api_key="INVALID_KEY")
    assert response.status_code == 401

def test_tc08_missing_api_key():
    """TC08: Hiányzó API kulcs"""
    response = get_with_custom_key("movie/popular")
    assert response.status_code == 401

# Érvénytelen bemenet validáció
def test_tc09_invalid_movie_id():
    """TC09: Érvénytelen film ID (-1)"""
    response = get_movie_details(-1)
    assert response.status_code in [400, 404]

def test_tc10_search_nonsense_query():
    """TC10: Értelmetlen keresési kifejezés"""
    response = search_movie("!!!@@@")
    assert response.status_code == 200
    data = response.json()
    assert len(data["results"]) == 0

def test_tc11_search_long_query():
    """TC11: 300 karakteres keresési kifejezés"""
    long_query = "a" * 300
    response = search_movie(long_query)
    assert response.status_code == 200

def test_tc12_empty_search_query():
    """TC12: Üres keresési string"""
    response = search_movie("")
    assert response.status_code in [200]
    data = response.json()
    assert len(data["results"]) == 0

# --2-pontos határérték-tesztek (BVA)--
# Dokumentáció alapján: Min:1, Max:500 oldalszám paraméter határok
# 100% határérték lefedettség

def test_tc13_boundary_min_invalid():
    """TC13: Alsó határ oldalszám-negatív"""
    response = get_popular_movies(page=0)
    assert response.status_code == 400

def test_tc14_boundary_min_valid():
    """TC14: Alsó határ oldalszám (page=1)"""
    response = get_popular_movies(page=1)
    assert response.status_code == 200

def test_tc15_boundary_max_valid():
    """TC15: Felső határ oldalszám (page=500)"""
    response = get_popular_movies(page=500)
    assert response.status_code == 200

def test_tc16_boundary_max_invalid():
    """TC16: Felső határ oldalszám-negatív (page=501)"""
    response = get_popular_movies(page=501)
    assert response.status_code == 400

# --Nem-funkcionális tesztek--
# Teljesítmény tesztek

def test_tc17_response_time():
    """TC17: Válaszidő < 2 másodperc"""
    import time
    start = time.time()
    response = get_popular_movies()
    elapsed = time.time() - start
    assert response.status_code == 200
    assert elapsed < 2.0

def test_tc18_response_size():
    """TC18: JSON válasz mérete < 1 MB"""
    response = get_popular_movies()
    size_mb = len(response.content) / (1024 * 1024)
    assert size_mb < 1.0

# Adat-integritás tesztek

def test_tc19_json_structure():
    """TC19: JSON struktúra ellenőrzése"""
    response = get_popular_movies()
    data = response.json()
    for movie in data["results"]:
        assert "id" in movie
        assert "title" in movie
        assert isinstance(movie["id"], int)

def test_tc20_data_types():
    """TC20: Adattípus ellenőrzés"""
    response = get_popular_movies()
    data = response.json()
    movie = data["results"][0]
    assert isinstance(movie["id"], int)
    assert isinstance(movie["title"], str)
    assert isinstance(movie.get("release_date"), (str, type(None)))