import requests

def fetch_poster_url(movie_id, api_key="your_tmdb_api_key_here"):
    """
    Fetches the poster URL for a given movie ID from TMDb.
    """
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        poster_path = data.get("poster_path")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return "https://via.placeholder.com/300x450.png?text=No+Image"
