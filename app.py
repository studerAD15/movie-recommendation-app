import streamlit as st
from recommender import get_recommendations
from utils.posters import fetch_poster
import pandas as pd

st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title("🎬 Movie Recommendation System")

# Load movie data
data = pd.read_csv("data/tmdb_5000_movies.csv")
movies = data['title'].values

# User input
selected_movie = st.selectbox("Select a movie you like:", movies)
genre_filter = st.selectbox("Filter by genre (optional):", ["All"] + sorted(set(g for gs in data['genres'] for g in eval(gs.replace("'", '"')) if 'name' in g)))

if st.button("Recommend"):
    recommendations = get_recommendations(selected_movie, genre_filter if genre_filter != "All" else None)
    if recommendations:
        cols = st.columns(5)
        for idx, (title, poster_url) in enumerate(recommendations):
            with cols[idx % 5]:
                st.image(poster_url, caption=title, use_column_width=True)
    else:
        st.error("No recommendations found.")

