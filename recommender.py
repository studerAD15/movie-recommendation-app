import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils.posters import fetch_poster

# Load dataset
df = pd.read_csv("data/tmdb_5000_movies.csv")
df = df.dropna(subset=['overview'])

# Combine genre into string
def extract_genres(genres_str):
    try:
        genres = eval(genres_str.replace("'", '"'))
        return " ".join([g['name'] for g in genres])
    except:
        return ""

df['genres_str'] = df['genres'].apply(extract_genres)

# TF-IDF on overview
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['overview'])
similarity = cosine_similarity(tfidf_matrix)

def get_recommendations(title, genre_filter=None, top_n=5):
    if title not in df['title'].values:
        return []
    idx = df[df['title'] == title].index[0]
    sim_scores = list(enumerate(similarity[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:]
    results = []
    for i, score in sim_scores:
        movie = df.iloc[i]
        if genre_filter and genre_filter not in movie['genres_str']:
            continue
        results.append((movie['title'], fetch_poster(movie['title'])))
        if len(results) >= top_n:
            break
    return results