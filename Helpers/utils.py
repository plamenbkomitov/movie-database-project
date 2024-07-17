def print_movie_details(movie):
    if movie:
        print(f"ID: {movie['id']}")
        print(f"Title: {movie['title']}")
        print(f"Description: {movie['description']}")
        print(f"Release Date: {movie['release_date']}")
        print(f"Director: {movie['director']}")
        print(f"Genre: {movie['genre_name']}")
        print(f"Likes: {movie['likes']}")
    else:
        print("Movie not found.")


def print_movie_list(movies):
    for movie in movies:
        print_movie_details(movie)
        print()
