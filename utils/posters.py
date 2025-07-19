import requests

# Fetches poster from OMDb API using the movie title
def fetch_poster(movie_title):
    api_key = "562c0dc8"  # Your OMDb API key
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={api_key}"
    
    try:
        response = requests.get(url)
        data = response.json()

        if data.get("Response") == "True" and data.get("Poster") and data["Poster"] != "N/A":
            return data["Poster"]
        else:
            return "https://via.placeholder.com/300x450?text=No+Image"
    
    except Exception as e:
        print(f"Error fetching poster: {e}")
        return "https://via.placeholder.com/300x450?text=Error"
