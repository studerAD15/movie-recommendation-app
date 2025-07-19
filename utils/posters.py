import requests
from urllib.parse import quote

def fetch_poster(movie_title):
    api_key = "562c0dc8"  # Replace with your OMDb or TMDb key if needed
    base_url = f"http://www.omdbapi.com/?t={quote(movie_title)}&apikey={api_key}"
    response = requests.get(base_url)
    if response.status_code == 200:
        data = response.json()
        return data.get("Poster", "https://via.placeholder.com/300x445?text=No+Image")
    return "https://via.placeholder.com/300x445?text=No+Image"
