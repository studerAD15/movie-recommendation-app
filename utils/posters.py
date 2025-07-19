import requests

OMDB_API_KEY = "562c0dc8"

def fetch_poster(title):
    try:
        url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200 and data.get("Response") == "True":
            poster_url = data.get("Poster")
            # Ensure the poster URL is valid and not "N/A"
            if poster_url and poster_url != "N/A":
                return poster_url
        return "https://via.placeholder.com/300x450.png?text=No+Image"
    except Exception as e:
        print(f"Error fetching poster for '{title}':", e)
        return "https://via.placeholder.com/300x450.png?text=Error"
