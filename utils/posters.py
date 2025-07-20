# utils/posters.py
import requests
import streamlit as st
from typing import Optional

# Replace with your actual TMDB API key
TMDB_API_KEY = "562c0dc8
"  
TMDB_BASE_URL = "https://api.themoviedb.org/3"
POSTER_BASE_URL = "https://image.tmdb.org/t/p/w500"

@st.cache_data(ttl=3600)  # Cache for 1 hour to avoid repeated API calls
def fetch_poster(movie_title: str) -> Optional[str]:
    """
    Fetch movie poster URL from TMDB API
    Returns full poster URL or None if not found
    """
    if not movie_title or not TMDB_API_KEY or TMDB_API_KEY == "your_api_key_here":
        return None
    
    try:
        # Search for the movie
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
            # Get the first result
            movie = data['results'][0]
            poster_path = movie.get('poster_path')
            
            if poster_path:
                # Return full poster URL
                return f"{POSTER_BASE_URL}{poster_path}"
        
        return None
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster for {movie_title}: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error fetching poster for {movie_title}: {e}")
        return None

# Alternative function using your existing CSV data if it has poster paths
def get_poster_from_csv(df, movie_title: str) -> Optional[str]:
    """
    Get poster URL from CSV data if available
    Assumes your CSV might have poster_path column
    """
    try:
        movie_row = df[df['title'].str.lower() == movie_title.lower()]
        if not movie_row.empty:
            poster_path = movie_row.iloc[0].get('poster_path')
            if poster_path and isinstance(poster_path, str):
                if poster_path.startswith('/'):
                    return f"{POSTER_BASE_URL}{poster_path}"
                elif poster_path.startswith('http'):
                    return poster_path
        return None
    except Exception:
        return None

# Fallback function with multiple strategies
def fetch_poster_robust(movie_title: str, csv_df=None) -> Optional[str]:
    """
    Robust poster fetching with multiple fallback strategies
    """
    # Strategy 1: Try CSV data first (faster)
    if csv_df is not None:
        poster_url = get_poster_from_csv(csv_df, movie_title)
        if poster_url:
            return poster_url
    
    # Strategy 2: Try TMDB API
    poster_url = fetch_poster(movie_title)
    if poster_url:
        return poster_url
    
    # Strategy 3: Return None (will trigger fallback UI)
    return None