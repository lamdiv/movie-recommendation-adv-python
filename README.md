# Movie Recommendation System

Movie recommendation system using the MovieLens dataset with two recommendation approaches: genre-based and user similarity-based filtering.

## Dataset

MovieLens Latest Small dataset:
- `movies.csv` - Movie IDs, titles, and genres (pipe-separated)
- `ratings.csv` - User IDs, movie IDs, and ratings (0.5-5.0 scale)

Attribution: GroupLens Research. For research and educational purposes only.

## Requirements

- Python 3.11
- pandas >= 1.5.0

```bash
pip install -r requirements.txt
```

## Project Structure

```
MovieRecommendation/
├── movie.py                        # Movie class definition
├── data_loader.py                  # Data loading with pandas
├── recommender.py                   # Base Recommender abstract class
├── genre_recommender.py            # GenreRecommender subclass
├── user_similarity_recommender.py # UserSimilarityRecommender subclass
├── main.py                         # Demonstration script
├── requirements.txt               # Python dependencies
└── dataset/                        # MovieLens dataset files
    ├── movies.csv
    └── ratings.csv
```

## Implementation

### Data Handling & Classes (15 pts)

**Movie Class** (`movie.py`):
- Attributes: `movie_id`, `title`, `genres`, `average_rating`
- Methods: `add_rating()`, `get_genres()`, `has_genre()`

**Data Loader** (`data_loader.py`):
- Uses pandas to load CSV files
- Creates mappings using dictionaries and sets:
  - `user_movie_mapping`: Dictionary mapping user_id → set of movie_ids they rated
  - `genre_movies`: Dictionary mapping genre → set of movie_ids
- Computes average ratings for each movie

### Recommendation Engine (30 pts)

**Base Recommender Class** (`recommender.py`):
- Abstract base class using `ABC` and `@abstractmethod`
- Common methods: `get_user_rated_movies()`, `get_top_movies_by_rating()`
- Abstract method: `recommend()`

**GenreRecommender** (`genre_recommender.py`):
- Inherits from `Recommender`
- Finds user's preferred genres based on their ratings
- Recommends top-rated movies from preferred genres
- Excludes movies the user has already rated

**UserSimilarityRecommender** (`user_similarity_recommender.py`):
- Inherits from `Recommender`
- Uses Jaccard similarity with set operations to find similar users:
  - `intersection = len(set1 & set2)`
  - `union = len(set1 | set2)`
  - `similarity = intersection / union`
- Recommends movies liked by similar users
- Ranks by popularity (how many similar users liked each movie)

### Design Patterns

- **Inheritance**: Base `Recommender` class with two concrete subclasses
- **Polymorphism**: Each subclass implements `recommend()` differently
- **Data Structures**: Extensive use of dictionaries and sets for efficient lookups

## Usage

```bash
python main.py
```

The demonstration script will:
1. Load the MovieLens dataset
2. Initialize both recommendation engines
3. Generate recommendations for a test user
4. Display user statistics and recommendations
5. Compare results from both systems

## How It Works

1. **Genre-Based Recommendations**:
   - Analyzes user's ratings to identify preferred genres
   - Finds top-rated movies in those genres
   - Excludes already-rated movies

2. **User Similarity Recommendations**:
   - Calculates Jaccard similarity between user and all other users
   - Finds the most similar users
   - Recommends movies liked by similar users, ranked by popularity