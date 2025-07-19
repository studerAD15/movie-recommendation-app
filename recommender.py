import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils.posters import fetch_poster_url

# Load data
data = pd.read_csv("data/tmdb_5000_movies.csv")

# Preprocess genres and keywords into one string
def create_soup(row):
    return ' '.join(eval(row['genres'].replace("'", '"'))[i]['name'] for i in range(len(eval(row['genres'].replace("'", '"'))))) + ' ' + row['keywords']

data['soup'] = data.apply(create_soup, axis=1)

# Vectorize and compute similarity
count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(data['soup'])
cosine_sim = cosine_similarity(count_matrix, count_matrix)

indices = pd.Series(data.index, index=data['title'].str.lower())

def get_recommendations(title):
    idx = indices[title.lower()]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:6]
    movie_indices = [i[0] for i in sim_scores]

    recommended_titles = data['title'].iloc[movie_indices].tolist()
    posters = [fetch_poster_url(title) for title in recommended_titles]

    return recommended_titles, posters
