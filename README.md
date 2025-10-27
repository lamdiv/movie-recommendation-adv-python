# Movie Recommendation System

A comprehensive movie recommendation system built with Python that provides personalized movie suggestions using collaborative filtering techniques. The system analyzes user preferences and movie ratings to generate recommendations through two complementary approaches:

- **Genre-Based Recommendations**: Identifies user's preferred genres based on their rating history and recommends highly-rated movies in those genres
- **User Similarity-Based Recommendations**: Uses Jaccard similarity to find users with similar tastes and recommends movies they've liked

The system features a fully interactive menu-driven interface that allows users to search movies, rate films, request personalized recommendations, and explore the recommendation algorithms.

## Quick Start

### Prerequisites
- Python 3.11 or higher
- pip package manager

### Installation Steps

1. **Navigate to the project directory**
   ```bash
   cd MovieRecommendation
   ```

2. **Create and activate virtual environment** (recommended)
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify dataset files are present**
   - `dataset/movies.csv`
   - `dataset/ratings.csv`

### Running the Application

Simply execute the main script:

```bash
python main.py
```

The program will:
1. Load the MovieLens dataset
2. Initialize recommendation engines
3. Run an automatic demo showing recommendations for a sample user
4. Launch an interactive menu where you can:
   - Request personalized recommendations
   - Search movies by title or genre
   - Rate movies to update your profile
   - View your rating history
   - Explore different recommendation algorithms

## Project Contributors

### Development Team

**Diwash Lamichhane**
- **Main Responsibilities:**
  - Data handling & classes implementation (Requirement 1)
  - Recommendation engine implementation (Requirement 2)
  - Search functionality (by title and genre)
  - Rating system and user profile management
  - Interactive menu-driven CLI design
  - Project documentation and README
  - Code integration and testing

**Suman Dangal**
- **Responsibilities:**
  - Recursive features implementation (Requirement 3)
  - Exception handling throughout the system (Requirement 4)
  - Error management and graceful failure handling
  - Code quality improvements

## Dataset

MovieLens Latest Small dataset (provided by GroupLens Research):
- `movies.csv` - Movie IDs, titles, and genres
- `ratings.csv` - User IDs, movie IDs, and ratings (0.5-5.0 scale)
- Dataset contains 9,742 movies and 100,836 ratings from 610 users

## Project Structure

```
MovieRecommendation/
├── main.py                         # Main application with interactive menu
├── movie.py                        # Movie class definition
├── data_loader.py                  # Data loading with pandas
├── recommender.py                  # Base Recommender abstract class
├── genre_recommender.py            # GenreRecommender subclass
├── user_similarity_recommender.py  # UserSimilarityRecommender subclass
├── requirements.txt                # Python dependencies
└── dataset/                        # MovieLens dataset files
    ├── movies.csv
    └── ratings.csv
```

## Features

### 1. Data Handling & Classes
- **Movie Class**: Complete movie representation with id, title, genres, average rating
- **Pandas Data Loading**: Efficient CSV parsing with error handling
- **Data Structures**: Dictionaries and sets for efficient lookups
  - User to movies mapping
  - Genre to movies mapping
  - User-movie rating dictionaries

### 2. Recommendation Engine
- **Abstract Base Class**: Using ABC and @abstractmethod for polymorphism
- **Genre-Based Recommender**: Suggests top-rated movies from user's preferred genres
- **User Similarity Recommender**: Uses Jaccard similarity with sets to find similar users and their favorite movies
- **Inheritance & Polymorphism**: Two concrete implementations of the Recommender interface

### 3. Recursive Features
- **Friends-of-Friends Search**: Recursive depth-first search through user similarity network
  - Configurable depth (1 = direct, 2 = friends-of-friends, 3+ = extended network)
  - Decay rate to weight distant connections
- **Recursive Menu System**: Menu function calls itself to return after each action
  - Enables continuous interaction without explicit loops
  - Graceful exit support

### 4. Exception Handling
- **Missing Dataset Files**: Clear error messages with suggestions
- **Invalid User Input**: Validation and helpful error messages
- **Empty Recommendations**: Detailed explanations for failed recommendations
- **CSV Parsing Errors**: Graceful handling of corrupted data
- **Keyboard Interrupts**: Clean application shutdown

### 5. Interactive Menu-Driven CLI
- **Request Recommendations**: Get personalized movie suggestions
- **Search Movies**: By title (partial match) or by genre
- **Rate Movies**: Update user profiles with new ratings
- **View Ratings**: See your complete rating history
- **Explore Algorithms**: Compare different recommendation approaches

## Implementation Details

### How It Works

1. **Data Loading**: 
   - Pandas loads CSV files
   - Creates Movie objects with computed average ratings
   - Builds user-movie and genre-movie mappings

2. **Genre-Based Recommendations**:
   - Analyzes user's ratings to identify preferred genres
   - Finds top-rated movies in those genres
   - Excludes already-rated movies

3. **User Similarity Recommendations**:
   - Calculates Jaccard similarity between users using set operations
   - Finds the most similar users
   - Recommends movies liked by similar users, ranked by popularity
   - Supports recursive depth search for extended user networks

4. **Interactive Features**:
   - Menu-driven navigation
   - Real-time profile updates when rating movies
   - Search with partial matching
   - Comprehensive error handling

### Key Algorithms

**Jaccard Similarity** (Used for finding similar users):
```python
similarity = intersection_size / union_size
intersection = len(set1 & set2)  # Users who rated same movies
union = len(set1 | set2)         # All unique movies rated
```

**Recursive Depth-First Search**:
```python
def dfs(current_user, remaining_depth, current_decay):
    # Find similar users
    # For each similar user with remaining depth:
        dfs(other_user, remaining_depth - 1, current_decay * decay_rate)
```

## License

This project is for educational purposes. The MovieLens dataset is provided by GroupLens Research under their research license.

## Acknowledgments

- **GroupLens Research** for the MovieLens dataset
- **Python** community for excellent libraries (pandas)
