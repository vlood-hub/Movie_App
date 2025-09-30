from sqlalchemy import create_engine, text

# Define the database URL
DB_URL = "sqlite:///data/users.db"

# Create the engine
engine = create_engine(DB_URL)#, echo=True)

# Create the movies table if it does not exist
with engine.connect() as connection:
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """))
    connection.commit()


def list_users():
    """Retrieve all users from the database."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT id, name FROM users"))
        users = result.fetchall()

    return [{"id": row[0], "name": row[1]} for row in users]


def add_user(name):
    """Add a new user to the database."""
    with engine.connect() as connection:
        try:
            connection.execute(text("INSERT INTO users (name) VALUES (:name)"),
                               {"name": name})
            connection.commit()
        except Exception as e:
            print(f"Error: {e}")


def delete_user(name):
    """Delete a user from the database."""
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users WHERE LOWER(name) = LOWER(:name)"),
                           {"name": name})
        connection.commit()


def update_user(new_name, old_name):
    """Update a user's name."""
    with engine.connect() as connection:
        connection.execute(text("UPDATE users SET name = :new_name WHERE name = :old_name"),
                           {"new_name": new_name, "old_name": old_name})
        connection.commit()
