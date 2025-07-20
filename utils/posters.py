# utils/posters.py

import requests
import streamlit as st
from typing import Optional

# ✅ Corrected API key (single-line string)
TMDB_API_KEY = "562c0dc8"
TMDB_BASE_URL = "https://api.themoviedb.org/3"
POSTER_BASE_URL = "https://image.tmdb.org/t/p/w500"

@st.cache_data(ttl=3600)
def fetch_poster(movie_title: str) -> Optional[str]:
    """Fetch movie poster URL from TMDB API."""
    if not movie_title or not TMDB_API_KEY or TMDB_API_KEY == "your_api_key_here":
        return None

    try:
        search_url = f"{TMDB_BASE_URL}/search/movie"
        params = {
            'api_key': TMDB_API_KEY,
            'query': movie_title,
            'page': 1
        }
        response = requests.get(search_url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        if data.get('results'):
            poster_path = data['results'][0].get('poster_path')
            if poster_path:
                return f"{POSTER_BASE_URL}{poster_path}"

        return None

    except requests.exceptions.RequestException as e:
        st.warning(f"Request error fetching poster for {movie_title}: {e}")
        return None
    except Exception as e:
        st.warning(f"Unexpected error fetching poster for {movie_title}: {e}")
        return None

def get_poster_from_csv(df, movie_title: str) -> Optional[str]:
    """Get poster URL from CSV data if available."""
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
    """Robust fallback poster fetching."""
    if csv_df is not None:
        poster = get_poster_from_csv(csv_df, movie_title)
        if poster:
            return poster

    poster = fetch_poster(movie_title)
    return poster
