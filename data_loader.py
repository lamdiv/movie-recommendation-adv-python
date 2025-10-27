import pandas as pd
from movie import Movie


def load_movies(movies_path):
    movies_df = pd.read_csv(movies_path)
    movies = {}
    
    for _, row in movies_df.iterrows():
        movie_id = int(row['movieId'])
        movies[movie_id] = Movie(
            movie_id=movie_id,
            title=row['title'],
            genres=row['genres']
        )
    
    return movies


def load_ratings_and_compute_averages(ratings_path, movies):
    ratings_df = pd.read_csv(ratings_path)
    user_ratings = {}
    
    for _, row in ratings_df.iterrows():
        user_id = int(row['userId'])
        movie_id = int(row['movieId'])
        rating = float(row['rating'])
        
        if movie_id in movies:
            movies[movie_id].add_rating(rating)
        
        if user_id not in user_ratings:
            user_ratings[user_id] = {}
        user_ratings[user_id][movie_id] = rating
    
    return user_ratings


def create_user_movie_mapping(user_ratings):
    user_movies = {}
    for user_id, ratings in user_ratings.items():
        user_movies[user_id] = set(ratings.keys())
    return user_movies


def create_genre_movies_mapping(movies):
    genre_movies = {}
    for movie_id, movie in movies.items():
        for genre in movie.get_genres():
            if genre not in genre_movies:
                genre_movies[genre] = set()
            genre_movies[genre].add(movie_id)
    
    return genre_movies


def load_data(movies_path, ratings_path):
    movies = load_movies(movies_path)
    user_ratings = load_ratings_and_compute_averages(ratings_path, movies)
    user_movie_mapping = create_user_movie_mapping(user_ratings)
    genre_movies_mapping = create_genre_movies_mapping(movies)
    
    return movies, user_ratings, user_movie_mapping, genre_movies_mapping