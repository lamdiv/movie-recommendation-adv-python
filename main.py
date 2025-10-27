from data_loader import load_data
from genre_recommender import GenreRecommender
from user_similarity_recommender import UserSimilarityRecommender


def print_movie_info(movie):
    print(f"  • {movie.title}")
    print(f"    Genres: {', '.join(movie.get_genres())}")
    print(f"    Average Rating: {movie.average_rating:.2f}")
    print(f"    Number of Ratings: {movie.total_ratings}")


def print_user_stats(user_id, movies, user_ratings):
    if user_id not in user_ratings:
        print(f"User {user_id} not found in the dataset.")
        return
    
    ratings = user_ratings[user_id]
    total_movies = len(ratings)
    avg_rating = sum(ratings.values()) / total_movies if total_movies > 0 else 0
    
    print(f"\n{'='*70}")
    print(f"USER {user_id} STATISTICS")
    print(f"{'='*70}")
    print(f"Total movies rated: {total_movies}")
    print(f"Average rating given: {avg_rating:.2f}")
    print(f"\nRecently rated movies:")
    
    count = 0
    for movie_id, rating in list(ratings.items())[:5]:
        if movie_id in movies:
            movie = movies[movie_id]
            print(f"  • {movie.title} - Rated: {rating}")
            count += 1
    
    if total_movies > 5:
        print(f"  ... and {total_movies - 5} more movies")


def demonstrate_genre_recommender(user_id, genre_recommender, movies, user_ratings):
    try:
        print(f"\n{'='*70}")
        print(f"GENRE-BASED RECOMMENDATIONS FOR USER {user_id}")
        print(f"{'='*70}")
        
        preferred_genres = genre_recommender.get_user_preferred_genres(user_id)
        
        if not preferred_genres:
            print("\nError: No preferred genres found. This may occur if:")
            print("  - User has no ratings")
            print("  - All user's ratings are below the minimum threshold")
            return
        
        if preferred_genres:
            print(f"\nUser's preferred genres:")
            for genre, avg_rating in list(preferred_genres.items())[:5]:
                print(f"  • {genre}: {avg_rating:.2f} average rating")
        
        recommendations = genre_recommender.recommend(user_id, n=10)
        
        if not recommendations:
            print("\nError: No recommendations available. This may occur if:")
            print("  - No movies match the user's preferred genres")
            print("  - User has already rated all movies in their preferred genres")
            return
        
        if recommendations:
            print(f"\nTop 10 Recommended Movies:")
            for i, movie in enumerate(recommendations, 1):
                print(f"\n{i}. Movie ID: {movie.movie_id}")
                print_movie_info(movie)
    except Exception as e:
        print(f"\nError generating recommendations: {e}")
        print("Please try again or choose a different option.")


def demonstrate_user_similarity_recommender(user_id, user_similarity_recommender, movies, user_ratings, recursive_depth=1):
    try:
        print(f"\n{'='*70}")
        print(f"USER SIMILARITY-BASED RECOMMENDATIONS FOR USER {user_id}")
        print(f"{'='*70}")
        
        if recursive_depth > 1:
            print(f"\nUsing recursive search with depth {recursive_depth} (friends of friends...)")
            similar_users = user_similarity_recommender.find_similar_users_recursive(user_id, depth=recursive_depth, max_neighbors=10)
        else:
            similar_users = user_similarity_recommender.find_similar_users(user_id, n=5)
        
        if not similar_users:
            print("\nError: No similar users found. Recommendations cannot be generated.")
            return
        
        if similar_users:
            print(f"\nMost Similar Users:")
            for similar_user_id, similarity in similar_users:
                print(f"  • User {similar_user_id}: {similarity*100:.1f}% similar")
        
        recommendations = user_similarity_recommender.recommend(user_id, n=10, recursive_depth=recursive_depth)
        
        if not recommendations:
            print("\nError: No recommendations available. This may occur if:")
            print("  - No similar users found")
            print("  - Similar users haven't rated any movies you haven't rated")
            print("  - All candidate movies were filtered out")
            return
        
        if recommendations:
            print(f"\nTop 10 Recommended Movies (liked by similar users):")
            for i, movie in enumerate(recommendations, 1):
                print(f"\n{i}. Movie ID: {movie.movie_id}")
                print_movie_info(movie)
        else:
            print("\nError: No recommendations available.")
    except Exception as e:
        print(f"\nError generating recommendations: {e}")
        print("Please try again or choose a different option.")


def search_movies_by_title(movies, search_term):
    """Search movies by title (case-insensitive partial match)."""
    search_term_lower = search_term.lower()
    matches = []
    
    for movie_id, movie in movies.items():
        if search_term_lower in movie.title.lower():
            matches.append(movie)
    
    return matches


def search_movies_by_genre(movies, genre_movies, genre):
    """Search movies by genre."""
    genre_lower = genre.lower()
    
    # First, try exact case-insensitive match
    matching_genre = None
    for g in genre_movies.keys():
        if g.lower() == genre_lower:
            matching_genre = g
            break
    
    if not matching_genre:
        # If no exact match, try partial match
        for g in genre_movies.keys():
            if genre_lower in g.lower():
                matching_genre = g
                break
    
    if not matching_genre:
        return [], None
    
    movie_ids = genre_movies.get(matching_genre, set())
    matches = [movies[movie_id] for movie_id in movie_ids if movie_id in movies]
    
    return matches, matching_genre


def list_available_genres(genre_movies):
    """List all available genres in the dataset."""
    return sorted(genre_movies.keys())


def demonstrate_movie_search(movies, genre_movies):
    """Demonstrate movie search by title or genre."""
    print(f"\n{'='*70}")
    print("MOVIE SEARCH")
    print(f"{'='*70}")
    print("\nSearch Options:")
    print("1. Search by title")
    print("2. Search by genre")
    print("3. List all genres")
    print("4. Back to main menu")
    
    choice = input("\nEnter choice: ").strip()
    
    if choice == '1':
        search_term = input("Enter title (or part of title) to search: ").strip()
        if not search_term:
            print("Search term cannot be empty.")
            return
        
        results = search_movies_by_title(movies, search_term)
        
        if not results:
            print(f"\nNo movies found matching '{search_term}'")
        else:
            print(f"\nFound {len(results)} movie(s) matching '{search_term}':")
            for i, movie in enumerate(results[:20], 1):  # Limit to first 20
                print(f"\n{i}. Movie ID: {movie.movie_id}")
                print_movie_info(movie)
            if len(results) > 20:
                print(f"\n... and {len(results) - 20} more results")
    
    elif choice == '2':
        genre = input("Enter genre to search: ").strip()
        if not genre:
            print("Genre cannot be empty.")
            return
        
        results, matched_genre = search_movies_by_genre(movies, genre_movies, genre)
        
        if not results or matched_genre is None:
            print(f"\nNo movies found for genre '{genre}'")
            print("Use option 3 to see available genres.")
        else:
            print(f"\nFound {len(results)} movie(s) in genre '{matched_genre}':")
            for i, movie in enumerate(results[:20], 1):  # Limit to first 20
                print(f"\n{i}. Movie ID: {movie.movie_id}")
                print_movie_info(movie)
            if len(results) > 20:
                print(f"\n... and {len(results) - 20} more results")
    
    elif choice == '3':
        genres = list_available_genres(genre_movies)
        print(f"\nAvailable genres in dataset ({len(genres)}):")
        for i, genre in enumerate(genres, 1):
            movie_count = len(genre_movies.get(genre, set()))
            print(f"  {i}. {genre} ({movie_count} movies)")
    
    elif choice == '4':
        return
    
    else:
        print("Invalid choice")


def compare_recommenders(user_id, genre_recommender, user_similarity_recommender, movies, user_ratings):
    print(f"\n{'='*70}")
    print(f"COMPARISON: DIFFERENT RECOMMENDERS FOR USER {user_id}")
    print(f"{'='*70}")
    
    genre_recs = set(movie.movie_id for movie in genre_recommender.recommend(user_id, n=10))
    similarity_recs = set(movie.movie_id for movie in user_similarity_recommender.recommend(user_id, n=10))
    
    overlap = genre_recs & similarity_recs
    only_genre = genre_recs - similarity_recs
    only_similarity = similarity_recs - genre_recs
    
    print(f"\nOverlapping recommendations: {len(overlap)}")
    if overlap:
        print("  Movies:")
        for movie_id in list(overlap)[:5]:
            if movie_id in movies:
                print(f"    • {movies[movie_id].title}")
    
    print(f"\nOnly in Genre Recommender: {len(only_genre)}")
    if only_genre:
        print("  Sample movies:")
        for movie_id in list(only_genre)[:3]:
            if movie_id in movies:
                print(f"    • {movies[movie_id].title}")
    
    print(f"\nOnly in Similarity Recommender: {len(only_similarity)}")
    if only_similarity:
        print("  Sample movies:")
        for movie_id in list(only_similarity)[:3]:
            if movie_id in movies:
                print(f"    • {movies[movie_id].title}")
def main_menu(genre_recommender, user_similarity_recommender, movies, user_ratings, genre_movies):
    try:
        print("\nMAIN MENU")
        print("1. Show genre-based demo")
        print("2. Show user-similarity demo")
        print("3. Compare recommenders")
        print("4. Interactive user-similarity (choose depth)")
        print("5. Search movies (by title or genre)")
        print("6. Show movie info by id")
        print("7. Exit")

        choice = input("Enter choice: ").strip()
        if choice == '1':
            try:
                user_id = int(input('Enter user id (blank for first user): ').strip() or min(user_ratings.keys()))
            except Exception:
                user_id = min(user_ratings.keys())
            if user_id not in user_ratings:
                print(f'User {user_id} not found. Using first available user.')
                user_id = min(user_ratings.keys())
            demonstrate_genre_recommender(user_id, genre_recommender, movies, user_ratings)
            return main_menu(genre_recommender, user_similarity_recommender, movies, user_ratings, genre_movies)
        elif choice == '2':
            try:
                user_id = int(input('Enter user id (blank for first user): ').strip() or min(user_ratings.keys()))
            except Exception:
                user_id = min(user_ratings.keys())
            if user_id not in user_ratings:
                print(f'User {user_id} not found. Using first available user.')
                user_id = min(user_ratings.keys())
            demonstrate_user_similarity_recommender(user_id, user_similarity_recommender, movies, user_ratings)
            return main_menu(genre_recommender, user_similarity_recommender, movies, user_ratings, genre_movies)
        elif choice == '3':
            try:
                user_id = int(input('Enter user id (blank for first user): ').strip() or min(user_ratings.keys()))
            except Exception:
                user_id = min(user_ratings.keys())
            if user_id not in user_ratings:
                print(f'User {user_id} not found. Using first available user.')
                user_id = min(user_ratings.keys())
            compare_recommenders(user_id, genre_recommender, user_similarity_recommender, movies, user_ratings)
            return main_menu(genre_recommender, user_similarity_recommender, movies, user_ratings, genre_movies)
        elif choice == '4':
            try:
                user_id = int(input('Enter user id (blank for first user): ').strip() or min(user_ratings.keys()))
            except Exception:
                user_id = min(user_ratings.keys())
            if user_id not in user_ratings:
                print(f'User {user_id} not found. Using first available user.')
                user_id = min(user_ratings.keys())
            try:
                depth = int(input('Enter recursive depth (1 = direct, 2 = friends-of-friends): ').strip() or '2')
                if depth < 1:
                    depth = 1
            except Exception:
                depth = 2
            demonstrate_user_similarity_recommender(user_id, user_similarity_recommender, movies, user_ratings, recursive_depth=depth)
            return main_menu(genre_recommender, user_similarity_recommender, movies, user_ratings, genre_movies)
        elif choice == '5':
            demonstrate_movie_search(movies, genre_movies)
            return main_menu(genre_recommender, user_similarity_recommender, movies, user_ratings, genre_movies)
        elif choice == '6':
            try:
                movie_id_str = input('Enter movie id: ').strip()
                movie_id = int(movie_id_str)
            except Exception:
                print('Invalid movie id input. Please enter a numeric id.')
                return main_menu(genre_recommender, user_similarity_recommender, movies, user_ratings, genre_movies)

            if movie_id in movies:
                print_movie_info(movies[movie_id])
            else:
                print(f'Movie id {movie_id} not found in the dataset.')

            return main_menu(genre_recommender, user_similarity_recommender, movies, user_ratings, genre_movies)
        elif choice == '7':
            print('Exiting.')
            return
        else:
            print('Invalid choice')
            return main_menu(genre_recommender, user_similarity_recommender, movies, user_ratings, genre_movies)
    except KeyboardInterrupt:
        print('\nInterrupted. Exiting menu.')
        return


def main():
    print("\n" + "="*70)
    print("MOVIE RECOMMENDATION SYSTEM")
    print("="*70)

    print("\nLoading data...")
    try:
        movies, user_ratings, user_movie_mapping, genre_movies = load_data(
            'dataset/movies.csv',
            'dataset/ratings.csv'
        )
    except FileNotFoundError as e:
        print(f"Dataset file not found: {e}")
        print("Make sure the 'dataset' folder and CSV files are present.")
        return
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    print(f"✓ Loaded {len(movies)} movies")
    print(f"✓ Loaded ratings from {len(user_ratings)} users")
    print(f"✓ Mapped {len(genre_movies)} genres")

    print("\nInitializing recommendation engines...")
    genre_recommender = GenreRecommender(movies, user_ratings, genre_movies)
    user_similarity_recommender = UserSimilarityRecommender(
        movies, user_ratings, user_movie_mapping
    )
    print("✓ Initialized Genre Recommender")
    print("✓ Initialized User Similarity Recommender")

    test_user_id = 1

    if test_user_id not in user_ratings:
        print(f"\nUser {test_user_id} not found. Using first available user.")
        test_user_id = min(user_ratings.keys())

    print_user_stats(test_user_id, movies, user_ratings)
    demonstrate_genre_recommender(test_user_id, genre_recommender, movies, user_ratings)
    demonstrate_user_similarity_recommender(test_user_id, user_similarity_recommender, movies, user_ratings)
    compare_recommenders(test_user_id, genre_recommender, user_similarity_recommender, movies, user_ratings)

    print(f"\n{'='*70}")
    print("DEMONSTRATION COMPLETE")
    print(f"{'='*70}\n")

    try:
        main_menu(genre_recommender, user_similarity_recommender, movies, user_ratings, genre_movies)
    except KeyboardInterrupt:
        print('\nInterrupted. Exiting program.')
        return


if __name__ == "__main__":
    main()