import requests

api_key = "562c0dc8"

def fetch_poster_url(movie_title):
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    if 'Poster' in data and data['Poster'] != "N/A":
        return data['Poster']
    else:
        return "https://via.placeholder.com/300x450.png?text=No+Image"
