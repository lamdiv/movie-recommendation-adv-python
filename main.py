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
    print(f"\n{'='*70}")
    print(f"GENRE-BASED RECOMMENDATIONS FOR USER {user_id}")
    print(f"{'='*70}")
    
    preferred_genres = genre_recommender.get_user_preferred_genres(user_id)
    if preferred_genres:
        print(f"\nUser's preferred genres:")
        for genre, avg_rating in list(preferred_genres.items())[:5]:
            print(f"  • {genre}: {avg_rating:.2f} average rating")
    
    recommendations = genre_recommender.recommend(user_id, n=10)
    
    if recommendations:
        print(f"\nTop 10 Recommended Movies:")
        for i, movie in enumerate(recommendations, 1):
            print(f"\n{i}. Movie ID: {movie.movie_id}")
            print_movie_info(movie)
    else:
        print("\nNo recommendations available.")


def demonstrate_user_similarity_recommender(user_id, user_similarity_recommender, movies, user_ratings):
    print(f"\n{'='*70}")
    print(f"USER SIMILARITY-BASED RECOMMENDATIONS FOR USER {user_id}")
    print(f"{'='*70}")
    
    similar_users = user_similarity_recommender.find_similar_users(user_id, n=5)
    
    if similar_users:
        print(f"\nMost Similar Users:")
        for similar_user_id, similarity in similar_users:
            print(f"  • User {similar_user_id}: {similarity*100:.1f}% similar")
    
    recommendations = user_similarity_recommender.recommend(user_id, n=10)
    
    if recommendations:
        print(f"\nTop 10 Recommended Movies (liked by similar users):")
        for i, movie in enumerate(recommendations, 1):
            print(f"\n{i}. Movie ID: {movie.movie_id}")
            print_movie_info(movie)
    else:
        print("\nNo recommendations available.")


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
def main_menu(genre_recommender, user_similarity_recommender, movies, user_ratings):
    print("\nMAIN MENU")
    print("1. Show genre-based demo")
    print("2. Show user-similarity demo")
    print("3. Compare recommenders")
    print("4. Interactive user-similarity (choose depth)")
    print("5. Exit")

    choice = input("Enter choice: ").strip()
    if choice == '1':
        try:
            user_id = int(input('Enter user id (blank for first user): ').strip() or min(user_ratings.keys()))
        except Exception:
            user_id = min(user_ratings.keys())
        demonstrate_genre_recommender(user_id, genre_recommender, movies, user_ratings)
        return main_menu(genre_recommender, user_similarity_recommender, movies, user_ratings)
    elif choice == '2':
        try:
            user_id = int(input('Enter user id (blank for first user): ').strip() or min(user_ratings.keys()))
        except Exception:
            user_id = min(user_ratings.keys())
        demonstrate_user_similarity_recommender(user_id, user_similarity_recommender, movies, user_ratings)
        return main_menu(genre_recommender, user_similarity_recommender, movies, user_ratings)
    elif choice == '3':
        try:
            user_id = int(input('Enter user id (blank for first user): ').strip() or min(user_ratings.keys()))
        except Exception:
            user_id = min(user_ratings.keys())
        compare_recommenders(user_id, genre_recommender, user_similarity_recommender, movies, user_ratings)
        return main_menu(genre_recommender, user_similarity_recommender, movies, user_ratings)
    elif choice == '4':
        try:
            user_id = int(input('Enter user id (blank for first user): ').strip() or min(user_ratings.keys()))
        except Exception:
            user_id = min(user_ratings.keys())
        try:
            depth = int(input('Enter recursive depth (1 = direct, 2 = friends-of-friends): ').strip() or '2')
            if depth < 1:
                depth = 1
        except Exception:
            depth = 2
        demonstrate_user_similarity_recommender(user_id, user_similarity_recommender, movies, user_ratings, recursive_depth=depth)
        return main_menu(genre_recommender, user_similarity_recommender, movies, user_ratings)
    elif choice == '5':
        print('Exiting.')
        return
    else:
        print('Invalid choice')
        return main_menu(genre_recommender, user_similarity_recommender, movies, user_ratings)


def main():
    print("\n" + "="*70)
    print("MOVIE RECOMMENDATION SYSTEM")
    print("="*70)

    print("\nLoading data...")
    movies, user_ratings, user_movie_mapping, genre_movies = load_data(
        'dataset/movies.csv',
        'dataset/ratings.csv'
    )

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

    main_menu(genre_recommender, user_similarity_recommender, movies, user_ratings)


if __name__ == "__main__":
    main()