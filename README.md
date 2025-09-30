# Movies Database

## Description

**My Movies Database** is a command-line Python application for managing a personal movie collection with multi-user support.

It allows you to add, update, delete, search, and analyze movies stored locally for different users. The program includes features such as generating random movie suggestions, sorting and filtering movies, creating statistics, exporting the database as a personalized webpage, and visualizing ratings. Now, you can manage multiple users, each with their own distinct movie collection.

This project is designed for movie enthusiasts who want to maintain their own lightweight movie collection without relying on external apps or services.

---

## Features

* 👤 **Multi-user support** – manage separate collections for different users
* 🎬 **List movies** – display all movies in the selected user's database
* ➕ **Add movie** – add a new movie with details such as title and rating for a user
* ❌ **Delete movie** – remove a movie from a user's collection
* ✏️ **Update movie** – change a movie’s information for a user
* 📊 **Stats** – view statistics (e.g., count, averages, median) for a user's collection
* 🎲 **Random movie** – get a random movie suggestion from a user's collection
* 🔍 **Search movie** – find movies by title with fuzzy matching
* 📑 **Sort movies** – sort by rating or by year
* 🌐 **Generate website** – export a user's database as a personalized HTML webpage
* 🎛 **Filter movies** – show movies based on conditions (e.g., by rating, year)
* 📈 **Rating histogram** – visualize movie ratings for a user
* 🗃️ **User management** – add, delete, and update user profiles
* 🔄 **Switch user** – easily switch between different users
* 🏳️ **Country flags** – display country flags for movies (if available)
* 📝 **Movie notes** – add personal notes to each movie

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/vlood-hub/Movie_App.git
cd Movie_App
```

### 2. Install dependencies

Make sure you have Python 3.8+ installed. Then install required libraries:

```bash
pip install -r requirements.txt
```

---

## Usage

### Run the program

```bash
python movie_3.py
```

## User Menu

When you start the program, you’ll first see the user menu:

```
Select a user or modify the list:

1. Alice
2. Bob
3. Charlie

+. Create new user
-. Delete user
o. Update user name

Enter choice:
```

- Enter the number to select a user and manage their movie collection.
- Enter `+` to create a new user.
- Enter `-` to delete a user.
- Enter `o` to update a user's name.

After selecting a user, you’ll see the main movie management menu for that user.

### Navigate the menu

You’ll see the interactive menu:

```
********** [User's Name] Movies Database **********

Menu:
0. Exit
1. List movies
2. Add movie
3. Delete movie
4. Update movie
5. Stats
6. Random movie
7. Search movie
8. Movies sorted by rating or chronologically
9. Generate website
10. Filter movies
11. Create Rating Histogram
99. Switch user
```

Enter the number or symbol for the action you want to perform.

---

## Example Workflow

1. Select or create a user profile.
2. Add a few movies with ratings and notes.
3. List them to confirm they are saved.
4. Generate a personalized website for the selected user.
5. Create a rating histogram to visualize your ratings distribution.
6. Switch users to manage different collections.

---

## Contributing

Contributions are welcome!

1. Fork the repository
2. Create a branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m "Add new feature"`)
4. Push the branch (`git push origin feature/your-feature`)
5. Open a pull request

---

## License

This project is provided for personal and educational use.