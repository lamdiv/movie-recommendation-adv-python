class Movie:
    def __init__(self, movie_id, title, genres):
        self.movie_id = movie_id
        self.title = title
        self.genres = genres.split('|') if genres else []
        self.average_rating = 0.0
        self.total_ratings = 0
        self.rating_sum = 0.0
    
    def add_rating(self, rating):
        self.total_ratings += 1
        self.rating_sum += rating
        self.average_rating = self.rating_sum / self.total_ratings
    
    def get_genres(self):
        return self.genres
    
    def has_genre(self, genre):
        return genre in self.genres
    
    def __repr__(self):
        return f"Movie(id={self.movie_id}, title='{self.title}', avg_rating={self.average_rating:.2f})"
    
    def __hash__(self):
        return hash(self.movie_id)
    
    def __eq__(self, other):
        if isinstance(other, Movie):
            return self.movie_id == other.movie_id
        return False