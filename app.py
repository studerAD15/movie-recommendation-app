import streamlit as st
import pandas as pd
from recommender import get_recommendations
from utils.posters import fetch_poster_url

# Load movie data
data = pd.read_csv("data/tmdb_5000_movies.csv")

# Parse genres column
def extract_genres(genre_str):
    try:
        genres = eval(genre_str.replace("null", "None"))
        return [g['name'] for g in genres if isinstance(g, dict) and 'name' in g]
    except:
        return []

data['genres_list'] = data['genres'].apply(extract_genres)

# Sidebar title
st.markdown("<h1 style='color:#FFCC00;'>🎬 Movie Recommendation System</h1>", unsafe_allow_html=True)

# Genre filter
all_genres = sorted(set(g for genre_list in data['genres_list'] for g in genre_list))
genre_filter = st.selectbox("📂 Filter by genre (optional):", ["All"] + all_genres)

# Filtered movies
if genre_filter != "All":
    filtered_data = data[data['genres_list'].apply(lambda genres: genre_filter in genres)]
else:
    filtered_data = data

# Movie selection
movie_list = filtered_data['title'].values
selected_movie = st.selectbox("🎥 Choose a movie:", movie_list)

# Show recommendations button
if st.button("🎯 Show Recommendations"):
    st.markdown("## Recommended Movies:")
    titles, posters = get_recommendations(selected_movie, data)

    cols = st.columns(5)
    for i in range(len(titles)):
        with cols[i % 5]:
            st.markdown(f"**{titles[i]}**")
            st.image(posters[i], use_container_width=True)
