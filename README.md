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

### User Interaction (10 pts)

The system provides a **menu-driven CLI** with comprehensive search and rating functionality:

**Search by Title** (`search_movies_by_title()`):
- Case-insensitive partial matching
- Finds all movies containing the search term in their title
- Returns detailed movie information (genres, ratings, rating count)

**Search by Genre** (`search_movies_by_genre()`):
- Case-insensitive genre matching (exact or partial)
- Searches through genre-movie mappings for efficient lookup
- Lists all movies in the specified genre
- Provides helpful suggestions when genre not found

**Additional Features**:
- List all available genres with movie counts
- Show movie details by ID
- Handles empty results gracefully with helpful error messages

**Rating Movies & Profile Management** (`rate_movie()`, `view_user_ratings()`):
- Rate movies with values from 0.5 to 5.0 (in 0.5 increments)
- Create new users or update existing user profiles
- Automatically updates movie average ratings when rated
- Updates user-movie mappings for similarity calculations
- View user's rating history sorted by rating value
- Support for rating updates (changing previous ratings)

### Recursion (10 pts)

The system implements **two recursive features**:

**1. Recursive Search for "Friends of Friends"** (`user_similarity_recommender.py`):
- The `find_similar_users_recursive()` method implements a recursive depth-first search
- Finds similar users of similar users (up to configurable depth)
- Uses decay rate to weight distant connections less than direct connections
- Allows exploring user similarity networks beyond immediate neighbors
- Example: With depth=2, finds users similar to users who are similar to you

**2. Recursive Menu Navigation System** (`main.py`):
- The `main_menu()` function implements a recursive menu system
- After executing each menu option, it recursively calls itself to return to the menu
- Enables continuous interaction without explicit loop constructs
- Gracefully handles user input errors and returns to menu
- Supports exiting via user choice or keyboard interrupt

```python
# Recursive menu example
def main_menu(...):
    choice = input("Enter choice: ").strip()
    if choice == '1':
        # Execute action
        return main_menu(...)  # Recursive call
    # ...
```

### Exception Handling (10 pts)

The system handles **three+ types of errors gracefully**:

**1. Missing Dataset File** (`data_loader.py`, `main.py`):
- Catches `FileNotFoundError` when CSV files are missing
- Provides clear error messages with suggestions for resolution
- Handles incomplete or corrupted dataset files

**2. Invalid User Input** (`main.py`):
- Validates user ID and movie ID inputs
- Handles non-numeric inputs gracefully
- Detects invalid movie IDs not in dataset
- Provides helpful error messages and fallbacks

**3. Empty Recommendations** (`main.py`):
- Checks for empty recommendation lists before processing
- Provides detailed error messages explaining why recommendations failed:
  - No similar users found
  - All candidate movies already rated
  - No movies match preferred genres
- Handles cases where user has no ratings or ratings below threshold

**4. Additional Error Handling**:
- CSV parsing errors (`pd.errors.ParserError`)
- Empty data files (`pd.errors.EmptyDataError`)
- Invalid data types in CSV files (`ValueError`, `KeyError`)
- Keyboard interrupts for graceful shutdown
- Movie not found errors

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
6. Launch an interactive menu with options:
   - Show genre-based recommendations
   - Show user-similarity recommendations
   - Compare recommender systems
   - Interactive recursive depth exploration
   - **Search movies by title or genre**
   - **Rate a movie (update profile)**
   - **View user ratings**
   - Show movie details by ID
   - Exit

## How It Works

1. **Genre-Based Recommendations**:
   - Analyzes user's ratings to identify preferred genres
   - Finds top-rated movies in those genres
   - Excludes already-rated movies

2. **User Similarity Recommendations**:
   - **Standard mode**: Calculates Jaccard similarity between user and all other users
   - Finds the most similar users
   - Recommends movies liked by similar users, ranked by popularity
   - **Recursive mode** (depth > 1): Explores similar users of similar users
     - Uses depth-first search to traverse user similarity network
     - Applies decay rate to weight distant connections
     - Provides broader recommendation pool from extended user network

3. **Interactive Menu**:
   - Recursive menu system allows continuous interaction
   - Menu options return to main menu recursively after execution
   - Supports recursive depth configuration for user similarity searches

4. **Interactive Search**:
   - Search by title with partial matching (e.g., "batman" finds all Batman movies)
   - Search by genre with case-insensitive matching
   - List all available genres with movie counts
   - Browse search results with detailed movie information

5. **Rating & Profile Management**:
   - Users can rate movies with validation (0.5-5.0 scale)
   - System automatically creates new users when rating
   - Updates movie average ratings in real-time
   - Maintains user-movie mappings for similarity calculations
   - Supports viewing and updating user rating history

6. **Error Handling**:
   - All operations wrapped in try-except blocks
   - Graceful degradation when data is missing or invalid
   - Detailed error messages guide users to solutions