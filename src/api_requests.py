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