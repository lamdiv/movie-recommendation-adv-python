from recommender import Recommender


class GenreRecommender(Recommender):
    def __init__(self, movies, user_ratings, genre_movies):
        super().__init__(movies, user_ratings)
        self.genre_movies = genre_movies
    
    def get_user_preferred_genres(self, user_id, min_rating=3.5):
        if user_id not in self.user_ratings:
            return {}
        
        genre_ratings = {}
        
        for movie_id, rating in self.user_ratings[user_id].items():
            if rating >= min_rating and movie_id in self.movies:
                movie = self.movies[movie_id]
                for genre in movie.get_genres():
                    if genre not in genre_ratings:
                        genre_ratings[genre] = []
                    genre_ratings[genre].append(rating)
        
        genre_averages = {}
        for genre, ratings in genre_ratings.items():
            genre_averages[genre] = sum(ratings) / len(ratings)
        
        return dict(sorted(genre_averages.items(), key=lambda x: x[1], reverse=True))
    
    def recommend(self, user_id, n=10):
        preferred_genres = self.get_user_preferred_genres(user_id)
        
        if not preferred_genres:
            return []
        
        user_rated_movies = self.get_user_rated_movies(user_id)
        
        candidate_movie_ids = set()
        for genre in preferred_genres.keys():
            genre_movie_ids = self.genre_movies.get(genre, set())
            new_movies = genre_movie_ids - user_rated_movies
            candidate_movie_ids.update(new_movies)
        
        return self.get_top_movies_by_rating(candidate_movie_ids, n)