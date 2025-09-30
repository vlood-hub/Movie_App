import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')
#API_KEY = "5f6fe4f8"


def fetch_data(title):
    """ Fetches the movies data """
    api_url = f"http://www.omdbapi.com/?apikey={API_KEY}&t={title}"
    try:
        response = requests.get(api_url)
        movie_info = response.json()
        return movie_info

    except requests.exceptions.ConnectionError:
        print("API is not accessible. Check your internet connection")