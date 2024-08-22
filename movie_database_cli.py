import argparse
from db_init import init_db
from Models.Movie import Movie
from Helpers.utils import print_movie_details, print_movie_list


def handle_movlst(args):
    movies = Movie.get_all()
    print_movie_list(movies)


def handle_movdt(args):
    movie = Movie.get_by_id(args.movie_id)
    if movie:
        print_movie_details(movie)
    else:
        print(f"No movie found with ID: {args.movie_id}")


def handle_movsrch(args):
    movies = Movie.search_by_title(args.query)
    if movies:
        print_movie_list(movies)
    else:
        print(f"No movies found with title matching: {args.query}")


def handle_movadd(args):
    movie_id = Movie.add(args.title, args.description, args.release_date, args.director, args.genre)
    if movie_id is not None:
        print(f"Movie added successfully with ID: {movie_id}")
    else:
        print("Failed to add the movie.")


def handle_movfv(args):
    if Movie.get_by_id(args.movie_id):
        Movie.favourite_movie(args.movie_id)
        print(f"Movie with ID {args.movie_id} marked as favorite.")
    else:
        print(f"Movie with ID {args.movie_id} does not exist.")


def handle_movcat(args):
    if args.category == 'liked':
        movies = Movie.get_top_liked()
    elif args.category == 'newest':
        movies = Movie.get_newest()
    elif args.category == 'genre':
        if not args.genre_name:
            print("Usage: movcat genre <genre_name>")
            return
        movies = Movie.get_by_genre(args.genre_name)
    else:
        print("Invalid category. Choose from [liked, newest, genre]")
        return

    if movies:
        print_movie_list(movies)
    else:
        print(f"No movies found for category: {args.category}")


def handle_movcvr(args):
    if args.interaction == 'view':
        movie_cover = Movie.get_movie_cover(args.movie_id)
    elif args.interaction == 'add':
        if not args.image_url:
            print("Usage: movcvr <movie_id> add <image_url>")
            return

        cover_added = Movie.add_movie_cover_url(args.movie_id, args.image_url)
        if cover_added:
            print(f"Cover for movie with ID: {args.movie_id} was successfully added.")
        else:
            print("Failed to add movie cover.")
        return
    else:
        print("Invalid option. Choose from [view, add]")
        return

    if movie_cover:
        print(movie_cover)
    else:
        print(f"No cover found for movie with ID: {args.movie_id}. Add valid URL for the cover of your movie.")


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


def setup_movcvr(subparsers):
    movcvr_parser = subparsers.add_parser('movcvr', help="Add or view movie covers")
    movcvr_parser.add_argument('interaction', choices=['view', 'add'], help="Interact with movie cover")
    movcvr_parser.add_argument('movie_id', type=int, help="ID of the movie")
    movcvr_parser.add_argument('image_url', type=str, nargs='?', help="Genre name (required if interaction is 'add')")
    movcvr_parser.set_defaults(func=handle_movcvr)


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
    setup_movcvr(subparsers)

    return parser


def main():
    init_db()
    parser = setup_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
