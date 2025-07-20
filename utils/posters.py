import requests
import streamlit as st
from typing import Optional

OMDB_API_KEY = "562c0dc8"
OMDB_BASE_URL = "http://www.omdbapi.com/"
POSTER_BASE_URL = "https://image.tmdb.org/t/p/w500"  # for CSV fallback only

@st.cache_data(ttl=3600)
def fetch_poster(movie_title: str) -> Optional[str]:
    """Fetch movie poster from OMDb using title."""
    if not movie_title or not OMDB_API_KEY:
        return None

    try:
        params = {
            "t": movie_title,
            "apikey": OMDB_API_KEY
        }
        response = requests.get(OMDB_BASE_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        if data.get("Response") == "True" and data.get("Poster") != "N/A":
            return data["Poster"]
        return None

    except requests.exceptions.RequestException as e:
        st.warning(f"Request error fetching poster for {movie_title}: {e}")
        return None
    except Exception as e:
        st.warning(f"Unexpected error fetching poster for {movie_title}: {e}")
        return None

def get_poster_from_csv(df, movie_title: str) -> Optional[str]:
    """Get poster from local CSV (fallback)."""
    try:
        movie_row = df[df['title'].str.lower() == movie_title.lower()]
        if not movie_row.empty:
            poster_path = movie_row.iloc[0].get('poster_path')
            if poster_path:
                if poster_path.startswith('/'):
                    return f"{POSTER_BASE_URL}{poster_path}"
                elif poster_path.startswith('http'):
                    return poster_path
        return None
    except Exception:
        return None

def fetch_poster_robust(movie_title: str, csv_df=None) -> Optional[str]:
    """Try CSV first, fallback to OMDb."""
    if csv_df is not None:
        poster = get_poster_from_csv(csv_df, movie_title)
        if poster:
            return poster

    return fetch_poster(movie_title)
