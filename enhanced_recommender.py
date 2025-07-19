import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from utils.posters import fetch_poster
import requests
import ast
from fuzzywuzzy import fuzz, process
from typing import List, Tuple, Dict, Any
import streamlit as st

class ImprovedRecommender:
    def __init__(self):
        self.movies_df = None
        self.similarity_matrix = None
        self.movie_features = None
        self.load_and_process_data()
    
    @st.cache_data(ttl=3600)
    def load_and_process_data(_self):
        """Load CSV data and create proper similarity matrix"""
        # Load your existing CSV
        _self.movies_df = pd.read_csv('data/tmdb_5000_movies.csv')
        
        # Create movie features for better recommendations
        _self._create_movie_features()
        _self._compute_similarity_matrix()
        
        return _self.movies_df
    
    def safe_eval(self, x):
        """Safely evaluate string representations of lists/dicts"""
        if pd.isna(x):
            return []
        try:
            return ast.literal_eval(x)
        except:
            return []
    
    def extract_elements(self, obj_list, key='name', limit=5):
        """Extract names from list of dictionaries"""
        if not obj_list:
            return []
        names = []
        for obj in obj_list[:limit]:
            if isinstance(obj, dict) and key in obj:
                names.append(obj[key])
        return names
    
    def _create_movie_features(self):
        """Create enhanced features from your CSV data"""
        df = self.movies_df.copy()
        
        # Process genres (assuming they're in JSON-like format)
        if 'genres' in df.columns:
            df['genres_list'] = df['genres'].apply(self.safe_eval)
            df['genres_clean'] = df['genres_list'].apply(lambda x: self.extract_elements(x))
            df['genres_str'] = df['genres_clean'].apply(lambda x: ' '.join(x).lower())
        else:
            df['genres_str'] = ''
        
        # Process keywords (if available)
        if 'keywords' in df.columns:
            df['keywords_list'] = df['keywords'].apply(self.safe_eval)
            df['keywords_clean'] = df['keywords_list'].apply(lambda x: self.extract_elements(x, limit=10))
            df['keywords_str'] = df['keywords_clean'].apply(lambda x: ' '.join(x).lower())
        else:
            df['keywords_str'] = ''
        
        # Process production companies (if available)
        if 'production_companies' in df.columns:
            df['companies_list'] = df['production_companies'].apply(self.safe_eval)
            df['companies_clean'] = df['companies_list'].apply(lambda x: self.extract_elements(x, limit=3))
            df['companies_str'] = df['companies_clean'].apply(lambda x: ' '.join(x).lower())
        else:
            df['companies_str'] = ''
        
        # Clean overview
        if 'overview' in df.columns:
            df['overview_clean'] = df['overview'].fillna('').str.lower()
        else:
            df['overview_clean'] = ''
        
        # Combine all features
        df['combined_features'] = (
            df['genres_str'] + ' ' + 
            df['keywords_str'] + ' ' + 
            df['companies_str'] + ' ' + 
            df['overview_clean']
        ).str.strip()
        
        self.movies_df = df
        self.movie_features = df[['title', 'combined_features', 'genres_clean', 'vote_average', 'popularity']].copy()
    
    def _compute_similarity_matrix(self):
        """Compute similarity matrix using TF-IDF"""
        # Create TF-IDF matrix
        tfidf = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=2
        )
        
        tfidf_matrix = tfidf.fit_transform(self.movies_df['combined_features'])
        self.similarity_matrix = cosine_similarity(tfidf_matrix)
    
    def search_movies(self, query: str, limit: int = 10) -> List[str]:
        """Smart search with fuzzy matching"""
        if not query:
            return []
        
        movie_titles = self.movies_df['title'].tolist()
        matches = process.extract(query, movie_titles, limit=limit, scorer=fuzz.partial_ratio)
        return [match[0] for match in matches if match[1] > 50]
    
    def recommend(self, movie_title: str, num_recommendations: int = 5) -> List[Tuple[str, str, float]]:
        """Get recommendations with similarity scores"""
        # Find movie index
        movie_indices = self.movies_df[self.movies_df['title'].str.lower() == movie_title.lower()].index
        
        if len(movie_indices) == 0:
            # Try fuzzy matching
            matches = process.extract(movie_title, self.movies_df['title'].tolist(), limit=1, scorer=fuzz.ratio)
            if matches and matches[0][1] > 80:
                movie_indices = self.movies_df[self.movies_df['title'] == matches[0][0]].index
            else:
                return []
        
        movie_idx = movie_indices[0]
        
        # Get similarity scores
        sim_scores = list(enumerate(self.similarity_matrix[movie_idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:num_recommendations+1]
        
        recommendations = []
        for idx, score in sim_scores:
            title = self.movies_df.iloc[idx]['title']
            poster = fetch_poster(title)
            recommendations.append((title, poster, score))
        
        return recommendations
    
    def get_movies_by_genre(self, genre: str, limit: int = 10) -> List[Tuple[str, str]]:
        """Get movies by specific genre"""
        genre_movies = self.movies_df[
            self.movies_df['genres_str'].str.contains(genre.lower(), na=False)
        ].copy()
        
        # Sort by vote_average if available
        if 'vote_average' in genre_movies.columns:
            genre_movies = genre_movies.sort_values('vote_average', ascending=False)
        
        selected_movies = genre_movies.head(limit)
        
        recommendations = []
        for _, row in selected_movies.iterrows():
            poster = fetch_poster(row['title'])
            recommendations.append((row['title'], poster))
        
        return recommendations
    
    def get_trending_movies(self, limit: int = 6) -> List[Tuple[str, str]]:
        """Get trending movies based on popularity/rating"""
        trending_df = self.movies_df.copy()
        
        # Sort by popularity or vote_average
        if 'popularity' in trending_df.columns:
            trending_df = trending_df.sort_values('popularity', ascending=False)
        elif 'vote_average' in trending_df.columns:
            trending_df = trending_df.sort_values('vote_average', ascending=False)
        else:
            # Random selection as fallback
            trending_df = trending_df.sample(n=min(limit*2, len(trending_df)))
        
        # Get top movies and add some randomness
        top_trending = trending_df.head(limit*2).sample(n=min(limit, len(trending_df)))
        
        recommendations = []
        for _, row in top_trending.iterrows():
            poster = fetch_poster(row['title'])
            recommendations.append((row['title'], poster))
        
        return recommendations
    
    def get_movie_details(self, movie_title: str) -> Dict[str, Any]:
        """Get detailed information about a movie from CSV"""
        movie_row = self.movies_df[self.movies_df['title'].str.lower() == movie_title.lower()]
        
        if movie_row.empty:
            return {'title': movie_title, 'error': 'Movie not found'}
        
        movie = movie_row.iloc[0]
        
        return {
            'title': movie.get('title', 'N/A'),
            'overview': movie.get('overview', 'No overview available'),
            'release_date': movie.get('release_date', 'N/A'),
            'vote_average': movie.get('vote_average', 'N/A'),
            'vote_count': movie.get('vote_count', 'N/A'),
            'popularity': movie.get('popularity', 'N/A'),
            'runtime': movie.get('runtime', 'N/A'),
            'budget': movie.get('budget', 'N/A'),
            'revenue': movie.get('revenue', 'N/A'),
            'genres': movie.get('genres_clean', []),
            'poster': fetch_poster(movie.get('title', ''))
        }
    
    def get_top_rated_movies(self, limit: int = 10) -> List[Tuple[str, str, float]]:
        """Get top rated movies"""
        if 'vote_average' not in self.movies_df.columns:
            return self.get_trending_movies(limit)
        
        # Filter movies with decent number of votes
        min_votes = self.movies_df['vote_count'].quantile(0.6) if 'vote_count' in self.movies_df.columns else 0
        
        top_movies = self.movies_df[
            self.movies_df['vote_count'] >= min_votes
        ].sort_values('vote_average', ascending=False).head(limit)
        
        recommendations = []
        for _, row in top_movies.iterrows():
            poster = fetch_poster(row['title'])
            recommendations.append((row['title'], poster, row['vote_average']))
        
        return recommendations
    
    def get_available_genres(self) -> List[str]:
        """Get list of all available genres"""
        all_genres = []
        for genres_list in self.movies_df['genres_clean']:
            all_genres.extend(genres_list)
        
        # Count frequency and return most common genres
        from collections import Counter
        genre_counts = Counter(all_genres)
        return [genre for genre, count in genre_counts.most_common(20)]