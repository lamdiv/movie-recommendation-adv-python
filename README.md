# Movie Recommendation System

A comprehensive movie recommendation system built with Python that provides personalized movie suggestions using collaborative filtering techniques. The system analyzes user preferences and movie ratings to generate recommendations through two complementary approaches:

- **Genre-Based Recommendations**: Identifies user's preferred genres based on their rating history and recommends highly-rated movies in those genres
- **User Similarity-Based Recommendations**: Uses Jaccard similarity to find users with similar tastes and recommends movies they've liked

The system features a fully interactive menu-driven interface that allows users to search movies, rate films, request personalized recommendations, and explore the recommendation algorithms.

## Project Contributors

### Developer

**Diwash Lamichhane**

**Role & Responsibilities:**
- Full-stack development of the recommendation system
- Implementation of genre-based and user similarity recommendation algorithms
- Design and implementation of the interactive menu-driven CLI
- Exception handling and error management throughout the system
- Recursive search algorithms for "friends-of-friends" similarity
- Search functionality (by title and genre)
- Rating system and user profile management
- Code documentation and README development
- Testing and validation of all features

**Technologies Used:**
- Python 3.11
- Pandas for data manipulation
- Object-oriented programming (OOP) principles
- Abstract base classes for design patterns
- Recursion and depth-first search algorithms

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

The system provides a **menu-driven CLI** with comprehensive search, rating, and recommendation functionality:

**Requesting Recommendations** (`request_recommendations()`):
- Primary menu option to get personalized movie recommendations
- Enter user ID to get custom recommendations
- Choose recommendation type:
  - Genre-based recommendations
  - User similarity-based recommendations
  - Both types side-by-side with overlap analysis
  - Recursive depth similarity search
- Handles new users gracefully with profile creation guidance
- Displays detailed movie information for each recommendation

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

## Installation & Setup

### Prerequisites
- Python 3.11 or higher
- pip package manager

### Installation Steps

1. **Clone or download the project**
   ```bash
   cd MovieRecommendation
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify dataset files**
   Ensure the `dataset/` folder contains:
   - `movies.csv`
   - `ratings.csv`

## How to Run

### Running the Application

Simply execute the main script:

```bash
python main.py
```

### Program Flow

When you run the application:

1. **Initialization Phase**
   - Loads movie data from `dataset/movies.csv`
   - Loads user ratings from `dataset/ratings.csv`
   - Initializes genre and similarity recommenders
   - Displays loading progress

2. **Automatic Demo Phase**
   - Shows statistics for user ID 1 (or first available user)
   - Displays genre-based recommendations
   - Displays user similarity-based recommendations
   - Compares both recommendation systems

3. **Interactive Menu**
   After the demo, you'll see a menu with the following options:
   
   - **1. Request recommendations** - Get personalized movie suggestions
   - **2. Show genre-based demo** - View genre recommendation algorithm
   - **3. Show user-similarity demo** - View similarity-based algorithm
   - **4. Compare recommenders** - Side-by-side comparison
   - **5. Interactive user-similarity** - Explore with recursive depth
   - **6. Search movies** - Search by title or genre
   - **7. Rate a movie** - Update your user profile
   - **8. View user ratings** - See your rating history
   - **9. Show movie info by id** - Get movie details
   - **10. Exit** - Quit the application

### Example Usage

**Getting Recommendations:**
```
Menu choice: 1
Enter your user ID: 5
Select recommendation type: 3 (Both)
→ See genre-based and similarity-based recommendations side-by-side
```

**Rating a Movie:**
```
Menu choice: 7
Enter your user ID: 5
Enter movie ID to rate: 1
Enter rating: 4.5
→ Movie rated and profile updated
```

**Searching Movies:**
```
Menu choice: 6
Search Options: 1 (Search by title)
Enter title: "batman"
→ Find all Batman movies
```

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

5. **Requesting Recommendations**:
   - Interactive menu allows users to request personalized recommendations
   - Flexible recommendation selection (genre, similarity, both, or recursive)
   - Side-by-side comparison shows overlapping recommendations
   - Handles new users with guidance on profile creation
   - Clean, user-friendly interface for getting movie suggestions

6. **Rating & Profile Management**:
   - Users can rate movies with validation (0.5-5.0 scale)
   - System automatically creates new users when rating
   - Updates movie average ratings in real-time
   - Maintains user-movie mappings for similarity calculations
   - Supports viewing and updating user rating history

7. **Error Handling**:
   - All operations wrapped in try-except blocks
   - Graceful degradation when data is missing or invalid
   - Detailed error messages guide users to solutions

## Required Files

All Python scripts necessary to run the application:

### Core Application Files

1. **`main.py`** - Main entry point of the application
   - Initializes the recommendation system
   - Implements the interactive menu-driven CLI
   - Handles user input and navigation
   - Contains functions for requesting recommendations, searching, and rating

2. **`movie.py`** - Movie class definition
   - Defines the Movie class with attributes: movie_id, title, genres
   - Maintains average rating and total ratings count
   - Methods: `add_rating()`, `get_genres()`, `has_genre()`

3. **`data_loader.py`** - Data loading functionality
   - Loads movies from CSV using pandas
   - Loads and processes user ratings
   - Creates user-movie mappings
   - Creates genre-movie mappings
   - Comprehensive error handling for missing/corrupted files

4. **`recommender.py`** - Base recommender class
   - Abstract base class using ABC and @abstractmethod
   - Common methods for all recommender types
   - Abstract method `recommend()` for subclasses to implement

5. **`genre_recommender.py`** - Genre-based recommendation engine
   - Subclass of Recommender
   - Analyzes user preferences by genre
   - Recommends top-rated movies from user's favorite genres

6. **`user_similarity_recommender.py`** - User similarity recommendation engine
   - Subclass of Recommender
   - Implements Jaccard similarity for finding similar users
   - Includes recursive "friends-of-friends" search algorithm
   - Recommends movies liked by similar users

### Configuration Files

7. **`requirements.txt`** - Python package dependencies
   - Lists all required Python packages (pandas)

8. **`README.md`** - This documentation file
   - Comprehensive project documentation
   - Installation and usage instructions

### Dataset Files (in `dataset/` folder)

9. **`dataset/movies.csv`** - Movie database
10. **`dataset/ratings.csv`** - User rating data

### Output

The application generates no additional files - all results are displayed in the terminal.

## License

This project is for educational purposes. The MovieLens dataset is provided by GroupLens Research under their research license.