from sqlalchemy import create_engine, text

# Define the database URL
DB_URL = "sqlite:///data/movies.db"

# Create the engine
engine = create_engine(DB_URL)#, echo=True)

# Create the movies table if it does not exist
with engine.connect() as connection:
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL,
            poster TEXT NOT NULL,
            note TEXT NOT NULL,
            UNIQUE(user_id, title)
        )
    """))
    connection.commit()


def list_movies():
    """Retrieve all movies from the database."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT user_id, title, year,rating, poster, note " \
                                            "FROM movies"))
        movies = result.fetchall()

    return {
        (row[0], row[1]): {
            "user_id": row[0],
            "year": row[2],
            "rating": row[3],
            "poster": row[4],
            "note": row[5]
        }
        for row in movies
    }


def add_movie(title, year, rating, poster, note, user_id):
    """Add a new movie to the database."""
    with engine.connect() as connection:
        try:
            connection.execute(text("INSERT INTO movies "
                                    "(user_id, title, year, rating, poster, note) " \
                                    "VALUES (:user_id, :title, :year, :rating, :poster, :note)"),
                                    {"user_id": user_id,
                                     "title": title,
                                     "year": year,
                                     "rating": rating,
                                     "poster": poster,
                                     "note": note
                                     }
                                    )
            connection.commit()
        except Exception as e:
            print(f"Error: {e}")


def delete_movie(title, user_id):
    """Delete a movie from the database."""
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM movies WHERE LOWER(title) = LOWER(:title) " \
                                "AND user_id = :user_id"),
                                {"title": title, "user_id": user_id})
        connection.commit()


def update_movie(title, note, user_id):
    """Update a movie's note in the database."""
    with engine.connect() as connection:
        connection.execute(text("UPDATE movies SET note = :note WHERE title = :title " \
                            "AND user_id = :user_id"),
                           {"note":note, "title":title, "user_id": user_id})
        connection.commit()
