import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from utils.posters import fetch_poster
import requests

# Load data
movies = pd.read_csv('data/tmdb_5000_movies.csv')
movie_titles = movies['title'].values

# Sample similarity matrix (replace with real similarity logic if needed)
similarity = cosine_similarity(np.random.rand(len(movie_titles), 10))

def recommend(movie_title):
    movie_title = movie_title.lower()
    idx = next((i for i, t in enumerate(movie_titles) if t.lower() == movie_title), None)
    if idx is None:
        return []
    scores = list(enumerate(similarity[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:6]
    recommended = []
    for i in scores:
        title = movie_titles[i[0]]
        poster = fetch_poster(title)
        recommended.append((title, poster))
    return recommended

def get_trending_movies():
    trending = movies.sample(6)['title'].tolist()
    trending_with_posters = [(title, fetch_poster(title)) for title in trending]
    return trending_with_posters
