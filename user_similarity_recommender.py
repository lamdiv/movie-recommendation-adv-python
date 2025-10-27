from recommender import Recommender


class UserSimilarityRecommender(Recommender):
    def __init__(self, movies, user_ratings, user_movie_mapping):
        super().__init__(movies, user_ratings)
        self.user_movie_mapping = user_movie_mapping
    
    def calculate_jaccard_similarity(self, set1, set2):
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        return intersection / union if union > 0 else 0.0
    
    def find_similar_users(self, user_id, n=20):
        if user_id not in self.user_movie_mapping:
            return []
        
        user_movies = self.user_movie_mapping[user_id]
        similarities = []
        
        for other_user_id, other_user_movies in self.user_movie_mapping.items():
            if other_user_id != user_id:
                similarity = self.calculate_jaccard_similarity(user_movies, other_user_movies)
                if similarity > 0:
                    similarities.append((other_user_id, similarity))
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:n]
    
    def get_movies_liked_by_users(self, user_ids, min_rating=3.5):
        movie_likes = {}
        
        for user_id in user_ids:
            if user_id in self.user_ratings:
                for movie_id, rating in self.user_ratings[user_id].items():
                    if rating >= min_rating:
                        movie_likes[movie_id] = movie_likes.get(movie_id, 0) + 1
        
        return movie_likes
    
    def recommend(self, user_id, n=10):
        similar_users = self.find_similar_users(user_id)
        
        if not similar_users:
            return []
        
        similar_user_ids = [user_id for user_id, _ in similar_users]
        movie_likes = self.get_movies_liked_by_users(similar_user_ids)
        
        if not movie_likes:
            return []
        
        user_rated_movies = self.get_user_rated_movies(user_id)
        candidate_movie_ids = set(movie_likes.keys()) - user_rated_movies
        
        candidates = []
        for movie_id in candidate_movie_ids:
            if movie_id in self.movies:
                candidates.append((self.movies[movie_id], movie_likes[movie_id]))
        
        candidates.sort(key=lambda x: (x[1], x[0].average_rating), reverse=True)
        
        return [movie for movie, _ in candidates[:n]]