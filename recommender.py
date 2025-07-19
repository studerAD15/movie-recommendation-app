import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from utils.posters import fetch_poster_url as fetch_poster


def get_recommendations(title, data, genre_filter=None, top_n=5):
    # Apply genre filter if selected
    if genre_filter and genre_filter != "All":
        def genre_match(genre_str):
            try:
                genres = eval(genre_str.replace("'", '"'))
                return any(g['name'] == genre_filter for g in genres if 'name' in g)
            except:
                return False

        filtered_data = data[data['genres'].apply(genre_match)]
    else:
        filtered_data = data

    # Check if title exists in filtered data
    if title not in filtered_data['title'].values:
        return [], []

    # Prepare TF-IDF matrix on 'overview'
    filtered_data['overview'] = filtered_data['overview'].fillna('')
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(filtered_data['overview'])

    # Compute cosine similarity
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Get index of selected movie
    idx = filtered_data[filtered_data['title'] == title].index[0]

    # Get similarity scores and top recommendations
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    top_indices = [i for i, _ in sim_scores[1:top_n + 1]]

    recommended_titles = filtered_data.iloc[top_indices]['title'].tolist()
    poster_urls = [fetch_poster(movie) for movie in recommended_titles]

    return recommended_titles, poster_urls
