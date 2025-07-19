import streamlit as st
from recommender import recommend, get_trending_movies
from utils.posters import fetch_poster
import pandas as pd

# Load movie list
movies_df = pd.read_csv("data/tmdb_5000_movies.csv")
movie_titles = movies_df['title'].tolist()

st.set_page_config(layout="wide")
st.title("🎬 Movie Recommendation System")

# 🔍 Movie Search with Dropdown Suggestion
st.markdown("## 🔎 Search by Movie Title")
selected_movie = st.selectbox("Type to search and select a movie", sorted(movie_titles))

# Recommendation Block
if selected_movie:
    recommended_movies = recommend(selected_movie)
    if recommended_movies:
        st.markdown("### 🎯 Recommended Movies")
        cols = st.columns(5)
        for idx, (title, poster) in enumerate(recommended_movies):
            with cols[idx % 5]:
                if poster:
                    st.image(poster, caption=title, use_container_width=True)
                else:
                    st.markdown(f"**{title}**\n\nNo poster available.")
    else:
        st.warning("No recommendations found.")

st.markdown("---")
st.markdown("## 🔥 Trending Now")

# Trending Movies
trending = get_trending_movies()
cols = st.columns(5)
for idx, (title, poster) in enumerate(trending):
    with cols[idx % 5]:
        if poster:
            st.image(poster, caption=title, use_container_width=True)
        else:
            st.markdown(f"**{title}**\n\nNo poster available.")
