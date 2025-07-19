import streamlit as st
import pandas as pd
import ast

from recommender import get_recommendations
from utils.posters import fetch_poster

# Load the movie dataset
data = pd.read_csv("data/tmdb_5000_movies.csv")

# Extract all genres from the 'genres' column
def extract_genres(genres_column):
    try:
        genres_list = ast.literal_eval(genres_column)
        return [g['name'] for g in genres_list if 'name' in g]
    except:
        return []

all_genres = sorted(set(
    genre
    for genre_list in data['genres']
    for genre in extract_genres(genre_list)
))

# Streamlit UI
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title("🎬 Movie Recommendation System")
st.markdown("Get recommendations based on your favorite movie!")

# Genre filter
genre_filter = st.selectbox("🎭 Filter by Genre (optional):", ["All"] + all_genres)

# Movie list (optionally filtered by genre)
if genre_filter != "All":
    filtered_movies = data[data['genres'].apply(lambda g: genre_filter in extract_genres(g))]
else:
    filtered_movies = data

movie_list = filtered_movies['title'].sort_values().tolist()
selected_movie = st.selectbox("🎞️ Choose a movie:", movie_list)

if st.button("🔍 Show Recommendations"):
    st.markdown("## Recommended Movies:")
    recommended_titles, poster_urls = get_recommendations(selected_movie, data)

    cols = st.columns(5)
    for i in range(len(recommended_titles)):
        with cols[i % 5]:
            st.image(poster_urls[i], caption=recommended_titles[i], use_column_width=True)
