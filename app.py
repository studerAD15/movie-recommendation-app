from recommender import get_recommendations
from streamlit_searchbox import st_searchbox
import streamlit as st
import pandas as pd

# Load movie data
movies_df = pd.read_csv("data/tmdb_5000_movies.csv")
movie_titles = movies_df["title"].tolist()

# Search function for searchbox
def search_movies(searchterm: str):
    return [movie for movie in movie_titles if searchterm.lower() in movie.lower()][:10]

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="centered")
st.title("🎬 Movie Recommendation System")
st.markdown("Search for your favorite movie and discover similar ones!")

# 🔍 Searchbox input
selected_movie = st_searchbox(
    search_movies,
    key="movie_searchbox",
    placeholder="Type a movie title...",
    label="Search Movie Title",
)

# Show recommendations
if selected_movie and st.button("🎯 Show Recommendations"):
    with st.spinner("Fetching recommendations..."):
        try:
            recommended_titles, poster_urls = get_recommendations(selected_movie)
            st.subheader(f"🎞️ Because you watched **{selected_movie}**")
            for title, poster in zip(recommended_titles, poster_urls):
                st.markdown(f"**{title}**")
                st.image(poster, use_container_width=True)

        except Exception as e:
            st.error(f"⚠️ Error: {str(e)}")
            st.error("Sorry, we couldn't find any recommendations for that movie.")
