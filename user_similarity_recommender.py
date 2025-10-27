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

    def find_similar_users_recursive(self, user_id, depth=2, max_neighbors=20, decay_rate=0.6):
        if depth <= 1:
            return self.find_similar_users(user_id, n=max_neighbors)

        if user_id not in self.user_movie_mapping:
            return []

        visited = set([user_id])
        weights = {}

        def dfs(current_user, remaining_depth, current_decay):
            current_movies = self.user_movie_mapping.get(current_user, set())
            for other_user, other_movies in self.user_movie_mapping.items():
                if other_user in visited:
                    continue
                sim = self.calculate_jaccard_similarity(current_movies, other_movies)
                if sim <= 0:
                    continue
                weight = sim * current_decay
                if weight > weights.get(other_user, 0):
                    weights[other_user] = weight
                if remaining_depth > 1:
                    visited.add(other_user)
                    dfs(other_user, remaining_depth - 1, current_decay * decay_rate)
                    visited.remove(other_user)

        dfs(user_id, depth, 1.0)

        results = sorted(weights.items(), key=lambda x: x[1], reverse=True)
        return results[:max_neighbors]
    
    def get_movies_liked_by_users(self, user_ids, min_rating=3.5):
        movie_likes = {}
        
        for user_id in user_ids:
            if user_id in self.user_ratings:
                for movie_id, rating in self.user_ratings[user_id].items():
                    if rating >= min_rating:
                        movie_likes[movie_id] = movie_likes.get(movie_id, 0) + 1
        
        return movie_likes
    
    def recommend(self, user_id, n=10, recursive_depth=1, decay_rate=0.6):
        if recursive_depth > 1:
            similar_users = self.find_similar_users_recursive(user_id, depth=recursive_depth, decay_rate=decay_rate)
        else:
            similar_users = self.find_similar_users(user_id)
        
        if not similar_users:
            return []

        similar_user_ids = [u_id for u_id, _ in similar_users]
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