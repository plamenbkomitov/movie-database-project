import argparse
from db_init import init_db
from Movie import Movie


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


def handle_movlst(args):
    movies = Movie.get_all()
    print_movie_list(movies)


def handle_movdt(args):
    movie = Movie.get_by_id(args.movie_id)
    print_movie_details(movie)


def handle_movsrch(args):
    movies = Movie.search_by_title(args.query)
    print_movie_list(movies)


def handle_movadd(args):
    Movie.add(args.title, args.description, args.release_date, args.director, args.genre)
    print("Movie added successfully.")


def handle_movfv(args):
    Movie.favourite_movie(args.movie_id)
    print("Movie marked as favorite.")


def handle_movcat(args):
    if args.category == 'liked':
        movies = Movie.get_top_liked()
        print_movie_list(movies)
    elif args.category == 'newest':
        movies = Movie.get_newest()
        print_movie_list(movies)
    elif args.category == 'genre':
        if not args.genre_name:
            print("Usage: movcat genre <genre_name>")
            return
        movies = Movie.get_by_genre(args.genre_name)
        print_movie_list(movies)
    else:
        print("Invalid category. Choose from [liked, newest, genre]")


def setup_movlst(subparsers):
    subparsers.add_parser('movlst', help="List all movies").set_defaults(func=handle_movlst)


def setup_movdt(subparsers):
    movdt_parser = subparsers.add_parser('movdt', help="Get movie details")
    movdt_parser.add_argument('movie_id', type=int, help="ID of the movie")
    movdt_parser.set_defaults(func=handle_movdt)


def setup_movsrch(subparsers):
    movsrch_parser = subparsers.add_parser('movsrch', help="Search movies by title")
    movsrch_parser.add_argument('query', type=str, help="Search query for movie titles")
    movsrch_parser.set_defaults(func=handle_movsrch)


def setup_movadd(subparsers):
    movadd_parser = subparsers.add_parser('movadd', help="Add a new movie")
    movadd_parser.add_argument('title', type=str, help="Title of the movie")
    movadd_parser.add_argument('description', type=str, help="Description of the movie")
    movadd_parser.add_argument('release_date', type=str, help="Release date of the movie (YYYY-MM-DD)")
    movadd_parser.add_argument('director', type=str, help="Director of the movie")
    movadd_parser.add_argument('genre', type=str, help="Genre of the movie")
    movadd_parser.set_defaults(func=handle_movadd)


def setup_movfv(subparsers):
    movfv_parser = subparsers.add_parser('movfv', help="Mark movie as favorite")
    movfv_parser.add_argument('movie_id', type=int, help="ID of the movie to mark as favorite")
    movfv_parser.set_defaults(func=handle_movfv)


def setup_movcat(subparsers):
    movcat_parser = subparsers.add_parser('movcat', help="Get movies by category")
    movcat_parser.add_argument('category', choices=['liked', 'newest', 'genre'], help="Category of movies")
    movcat_parser.add_argument('genre_name', type=str, nargs='?', help="Genre name (required if category is 'genre')")
    movcat_parser.set_defaults(func=handle_movcat)


def setup_parser():
    parser = argparse.ArgumentParser(description="Movie database CLI")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.required = True

    setup_movlst(subparsers)
    setup_movdt(subparsers)
    setup_movsrch(subparsers)
    setup_movadd(subparsers)
    setup_movfv(subparsers)
    setup_movcat(subparsers)

    return parser


def main():
    init_db()
    parser = setup_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
