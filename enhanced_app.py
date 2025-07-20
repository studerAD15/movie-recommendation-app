import streamlit as st
import plotly.express as px
from enhanced_recommender import ImprovedRecommender
import pandas as pd

# Initialize the improved recommender
@st.cache_resource
def load_recommender():
return ImprovedRecommender()

recommender = load_recommender()

# Page config
st.set_page_config(
page_title="🎬 Enhanced Movie Recommendations", 
layout="wide",
page_icon="🎬"
)

# Custom CSS
st.markdown("""
<style>
   .main-header {
       font-size: 3rem;
       font-weight: bold;
       text-align: center;
       color: #e74c3c;
       margin-bottom: 2rem;
   }
   .sub-header {
       font-size: 1.8rem;
       color: #2c3e50;
       margin: 1.5rem 0;
       border-left: 4px solid #3498db;
       padding-left: 1rem;
   }
   .movie-stats {
       background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
       padding: 1rem;
       border-radius: 10px;
       color: white;
       text-align: center;
       margin: 0.5rem;
   }
   .similarity-score {
       background: rgba(46, 204, 113, 0.1);
       padding: 0.3rem 0.6rem;
       border-radius: 15px;
       font-size: 0.85rem;
       color: #27ae60;
       font-weight: bold;
       display: inline-block;
       margin-top: 0.5rem;
   }
</style>
""", unsafe_allow_html=True)

# Main title
st.markdown('<h1 class="main-header">🎬 Enhanced Movie Recommendation System</h1>', unsafe_allow_html=True)

# Sidebar for navigation
st.sidebar.title("🎯 Navigation")
page = st.sidebar.selectbox("Choose a page:", [
"🏠 Home", 
"🔍 Smart Search", 
"🎭 Browse by Genre", 
"📊 Movie Analytics",
"⭐ Top Rated",
"🔥 Trending"
])

# Display dataset info in sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### 📈 Dataset Info")
total_movies = len(recommender.movies_df)
st.sidebar.metric("Total Movies", f"{total_movies:,}")

if 'vote_average' in recommender.movies_df.columns:
avg_rating = recommender.movies_df['vote_average'].mean()
st.sidebar.metric("Average Rating", f"{avg_rating:.1f}/10")

# ====================================================================================
# PAGE ROUTING
# ====================================================================================

if page == "🏠 Home":
# Movie search section
st.markdown('<h2 class="sub-header">🔍 Find Your Next Favorite Movie</h2>', unsafe_allow_html=True)

search_query = st.text_input("🎬 Search for a movie:", placeholder="Type movie name...")

if search_query:
search_results = recommender.search_movies(search_query, limit=8)
if search_results:
selected_movie = st.selectbox("📋 Select from search results:", search_results)
else:
st.warning("No movies found. Try a different search term.")
selected_movie = None
else:
# Show dropdown with all movies
all_movies = sorted(recommender.movies_df['title'].tolist())
selected_movie = st.selectbox("📋 Or select from all movies:", all_movies)

# Get recommendations
if selected_movie and st.button("🎯 Get Recommendations", type="primary"):
recommendations = recommender.recommend(selected_movie, num_recommendations=8)

if recommendations:
st.markdown(f'<h2 class="sub-header">🎬 Movies Similar to "{selected_movie}"</h2>', unsafe_allow_html=True)

# Display in grid
cols = st.columns(4)
for idx, (title, poster, similarity) in enumerate(recommendations):
with cols[idx % 4]:
if poster and "placeholder" not in poster:
st.image(poster, caption=title, use_container_width=True)
else:
st.markdown(f"### {title}")
st.write("🎬 No poster available")

# Show similarity score
st.markdown(f'<div class="similarity-score">Match: {similarity:.1%}</div>', 
unsafe_allow_html=True)

# Add movie details button
if st.button(f"📖 Details", key=f"details_{idx}"):
details = recommender.get_movie_details(title)
st.session_state.movie_details = details
else:
st.error("Sorry, couldn't find recommendations for this movie.")

# Show movie details if selected
if hasattr(st.session_state, 'movie_details'):
details = st.session_state.movie_details
st.markdown("---")
st.markdown("### 📖 Movie Details")

col1, col2 = st.columns([1, 2])
with col1:
if details.get('poster'):
st.image(details['poster'], width=300)

with col2:
st.write(f"**Title:** {details.get('title', 'N/A')}")
st.write(f"**Rating:** {details.get('vote_average', 'N/A')}/10")
st.write(f"**Release Date:** {details.get('release_date', 'N/A')}")
st.write(f"**Runtime:** {details.get('runtime', 'N/A')} minutes")
st.write(f"**Genres:** {', '.join(details.get('genres', []))}")
st.write(f"**Overview:** {details.get('overview', 'No overview available')}")

# Trending section
st.markdown("---")
st.markdown('<h2 class="sub-header">🔥 Trending Movies</h2>', unsafe_allow_html=True)
trending = recommender.get_trending_movies(limit=8)

cols = st.columns(4)
for idx, (title, poster) in enumerate(trending):
with cols[idx % 4]:
if poster and "placeholder" not in poster:
st.image(poster, caption=title, use_container_width=True)
else:
st.markdown(f"### {title}")

elif page == "🎭 Browse by Genre":
st.markdown('<h2 class="sub-header">🎭 Browse Movies by Genre</h2>', unsafe_allow_html=True)

available_genres = recommender.get_available_genres()
selected_genre = st.selectbox("Choose a genre:", available_genres)

if selected_genre:
genre_movies = recommender.get_movies_by_genre(selected_genre, limit=12)

st.markdown(f"### 🎬 {selected_genre} Movies")
cols = st.columns(4)

for idx, (title, poster) in enumerate(genre_movies):
with cols[idx % 4]:
if poster and "placeholder" not in poster:
st.image(poster, caption=title, use_container_width=True)
else:
st.markdown(f"### {title}")

elif page == "⭐ Top Rated":
st.markdown('<h2 class="sub-header">⭐ Top Rated Movies</h2>', unsafe_allow_html=True)

top_movies = recommender.get_top_rated_movies(limit=16)

cols = st.columns(4)
for idx, (title, poster, rating) in enumerate(top_movies):
with cols[idx % 4]:
if poster and "placeholder" not in poster:
st.image(poster, caption=f"{title} ⭐{rating}/10", use_container_width=True)
else:
st.markdown(f"### {title}")
st.write(f"⭐ {rating}/10")

elif page == "📊 Movie Analytics":
st.markdown('<h2 class="sub-header">📊 Movie Analytics</h2>', unsafe_allow_html=True)

# Create some basic analytics
df = recommender.movies_df

col1, col2, col3 = st.columns(3)

with col1:
st.markdown('<div class="movie-stats"><h3>Total Movies</h3><h2>' + 
f'{len(df):,}</h2></div>', unsafe_allow_html=True)

with col2:
if 'vote_average' in df.columns:
avg_rating = df['vote_average'].mean()
st.markdown('<div class="movie-stats"><h3>Avg Rating</h3><h2>' + 
f'{avg_rating:.1f}/10</h2></div>', unsafe_allow_html=True)

with col3:
if 'release_date' in df.columns:
latest_year = pd.to_datetime(df['release_date'], errors='coerce').dt.year.max()
st.markdown('<div class="movie-stats"><h3>Latest Movie</h3><h2>' + 
f'{int(latest_year) if not pd.isna(latest_year) else "N/A"}</h2></div>', 
unsafe_allow_html=True)

# Genre distribution
if 'genres_clean' in df.columns:
st.markdown("### 🎭 Genre Distribution")
all_genres = []
for genres in df['genres_clean']:
all_genres.extend(genres)

genre_counts = pd.Series(all_genres).value_counts().head(10)
fig = px.bar(x=genre_counts.index, y=genre_counts.values, 
title="Top 10 Movie Genres")
st.plotly_chart(fig, use_container_width=True)

# Rating distribution
if 'vote_average' in df.columns:
st.markdown("### ⭐ Rating Distribution")
fig = px.histogram(df, x='vote_average', nbins=20, 
title="Movie Rating Distribution")
st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("### 🎬 About This App")

st.write("This enhanced movie recommendation system uses content-based filtering to suggest movies similar to your preferences. Built with Streamlit and powered by the TMDB dataset.")

st.markdown("""
<style>
    .footer {
        font-size: 0.9rem;
        color: #6c757d;
        text-align: center;
        margin-top: 2rem;
    }
    .footer a {
        color: #3498db;
        text-decoration: none;
        font-weight: bold;
    }
</style>
<div class="footer">
    Made with ❤️ by <a href="https://www.linkedin.com/in/aditya-chhikara-9a7453306/" target="_blank">Aditya Chhikara</a>
</div>
""", unsafe_allow_html=True)