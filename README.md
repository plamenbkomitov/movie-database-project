# Movie Database Project

## Overview

The Movie Database Project is a command-line interface (CLI) application that allows users to manage a database of movies. This project supports various functionalities such as listing movies, retrieving movie details, searching movies by title, adding new movies, marking movies as favorites, and categorizing movies. The project uses SQLite as the database to store movie information and follows Object-Oriented Programming (OOP) principles for clean and maintainable code.

## Table of Contents

- [Setup](#setup)
- [Usage](#usage)
  - [List All Movies](#list-all-movies)
  - [Get Movie Details](#get-movie-details)
  - [Search Movies](#search-movies)
  - [Add a New Movie](#add-a-new-movie)
  - [Mark Movie as Favorite](#mark-movie-as-favorite)
  - [Get Movies by Category](#get-movies-by-category)
- [Database Structure](#database-structure)
- [Project Structure](#project-structure)
- [Predefined Genres](#predefined-genres)

## Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/movie-database-project.git
   cd movie-database-project
   ```
2. **Install dependencies**:
   Ensure you have Python installed. The required modules are part of the Python Standard Library, so no additional installations are necessary.

3. **Initialize the database**:
   The database initialization is handled automatically when you run the application for the first time.


## Usage

The CLI provides several commands to interact with the movie database. Below are the available commands and their descriptions:

### List All Movies

Lists all movies in the database.

```bash
python movie_database_cli.py movlst
```


### Get Movie Details

Retrieves detailed information about a specific movie by its ID.

```bash
# Command
python movie_database_cli.py movdt <movie_id>

# Example
python movie_database_cli.py movdt 1
```

### Search Movies

Searches for movies based on their titles.

```bash
# Command
python movie_database_cli.py movsrch <query>

# Example
python movie_database_cli.py movsrch "Inception"
```
### Add a New Movie

Adds a new movie to the database. You must provide the title, description, release date, director, and genre.

```bash
# Command
python movie_database_cli.py movadd <title> <desc> <date> <director> <genre>

# Example
python movie_database_cli.py movadd "Inception" "A mind-bending thriller" "2010-07-16" "Christopher Nolan" "Science Fiction"
```
### Mark Movie as Favorite

Marks a movie as a favorite by incrementing its like count.

```bash
# Command
python movie_database_cli.py movfv <movie_id>

# Example
python movie_database_cli.py movfv 1
```
### Get Movies by Category

Retrieves movies based on specified categories such as liked, newest, or genre. For genre, you need to specify the genre name.

```bash
# Command
python movie_database_cli.py movcat <category: [liked, newest, genre]> [genre_name]

# Examples
python movie_database_cli.py movcat liked
python movie_database_cli.py movcat newest
python movie_database_cli.py movcat genre "Action"
```

## Database Structure

The database consists of two main tables: Movies and Genres.

### Movies Table

- **id**: Integer, Primary Key, Auto-increment
- **title**: Text, Not Null, Max length 100
- **description**: Text, Not Null, Max length 500
- **release_date**: Date, Not Null
- **director**: Text, Not Null, Max length 50
- **genre_id**: Integer, Foreign Key references Genres(id)
- **likes**: Integer, Default 0

### Genres Table

- **id**: Integer, Primary Key, Auto-increment
- **name**: Text, Not Null, Unique, Max length 50

### Explanation

Both Movies and Genres tables are necessary to maintain a normalized database structure. The Genres table allows for easy management and categorization of genres, ensuring consistency and avoiding duplicate genre names. The Movies table references the Genres table via genre_id, creating a relationship that helps in categorizing and querying movies based on their genres efficiently.

## Project Structure

The project follows a modular structure to maintain separation of concerns and enhance readability.

```plaintext
movie-database-project/
│
├── Models/
│   ├── Movie.py
│   └── Genre.py
│
├── Helpers/
│   ├── constants.py
│   └── utils.py
│
├── db_init.py
└── movie_database_cli.py
```
## File Descriptions

- **Movie.py**: Contains the Movie class with methods for interacting with the Movies table in the database.
- **Genre.py**: Contains the Genre class with methods for interacting with the Genres table in the database.
- **db_init.py**: Handles the database connection and initialization.
- **movie_database_cli.py**: The main CLI application script that defines the available commands and their handlers.
- **constants.py**: Contains constant values used throughout the project, such as the database name and predefined genres.
- **utils.py**: Utility functions used throughout the project.
- **README.md**: Documentation for the project.

## Predefined Genres

The project includes a set of predefined genres to categorize movies. These genres are automatically inserted into the database during the initialization process. If a user tries to add a movie with a genre that does not exist in the predefined list, the system will default to the 'unknown' genre and notify the user.

### List of Predefined Genres

```
action, adventure, animation, biography, comedy, crime, disaster, documentary, drama, family, fantasy, film noir, historical, holiday, horror, musical, mystery, political, romance, satire, science fiction, slice of life, sport, superhero, surreal, teen, thriller, war, western, unknown
```

These genres ensure that movies are consistently categorized, making it easier for users to search and filter movies based on their interests.

