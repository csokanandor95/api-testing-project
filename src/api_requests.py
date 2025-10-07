import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

def get_popular_movies(page=1, language="en-US"):
    """Népszerű filmek lekérdezése"""
    url = f"{BASE_URL}/movie/popular"
    params = {"api_key": API_KEY, "page": page, "language": language}
    return requests.get(url, params=params)

def get_movie_details(movie_id):
    """Film részletek lekérdezése ID alapján"""
    url = f"{BASE_URL}/movie/{movie_id}"
    params = {"api_key": API_KEY}
    return requests.get(url, params=params)

def search_movie(query, page=1):
    """Film keresése név alapján"""
    url = f"{BASE_URL}/search/movie"
    params = {"api_key": API_KEY, "query": query, "page": page}
    return requests.get(url, params=params)

def get_movie_genres():
    """Filmműfajok listájának lekérdezése"""
    url = f"{BASE_URL}/genre/movie/list"
    params = {"api_key": API_KEY}
    return requests.get(url, params=params)

def get_with_custom_key(endpoint, api_key=None, **params):
    """Egyedi API kulccsal való hívás (hibás kulcs teszteléshez)"""
    url = f"{BASE_URL}/{endpoint}"
    if api_key:
        params["api_key"] = api_key
    return requests.get(url, params=params)