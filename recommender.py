from abc import ABC, abstractmethod


class Recommender(ABC):
    def __init__(self, movies, user_ratings):
        self.movies = movies
        self.user_ratings = user_ratings
    
    @abstractmethod
    def recommend(self, user_id, n=10):
        pass
    
    def get_user_rated_movies(self, user_id):
        if user_id in self.user_ratings:
            return set(self.user_ratings[user_id].keys())
        return set()
    
    def get_top_movies_by_rating(self, candidate_movie_ids, n):
        candidates = []
        for movie_id in candidate_movie_ids:
            if movie_id in self.movies:
                candidates.append(self.movies[movie_id])
        
        candidates.sort(key=lambda m: m.average_rating, reverse=True)
        return candidates[:n]