from termcolor import colored
from api import data_fetcher
from db_manager import movie_storage_sql as storage
import movie_3


def cmd_list_movies(user_movies, user_data):
    """ Retrieve and display all movies from the database. """
    print(f"{len(user_movies)} movies in total\n")
    print(f"{'Title (year)':<50} Rating\n")

    if not user_movies:
        print(f"📢 {user_data['name']}, your movie collection is empty. Add some movies!")
    else:
        for name, attributes in user_movies.items():
            left = f"{name} ({attributes['year']})"
            print(f"{left:<51}: {attributes['rating']}")


def cmd_add_movie(user_movies, user_data):
    """ The function adds a movie to the movies database and saves changes """
    while True:
        new_name = input("Enter new movie name: ")
        if new_name == "":
            print("Empty input")
        else:
            break

    if new_name in user_movies:
        print(colored("Movie",'red'), colored(new_name,'green'),
            colored("already exists",'red'))
    else:
        try:
            movie = data_fetcher.fetch_data(new_name)
            storage.add_movie(
                movie['Title'],
                movie['Year'],
                movie['imdbRating'],
                movie['Poster'],
                note='',
                user_id=user_data['id']
            )
            print(colored("Movie",'blue'), colored(movie['Title'],'green'),
                colored("successfully added",'blue'))
            movies = storage.list_movies()
            user_movies = {title: info for title, info in movies.items()
                       if info.get('user_id') == user_data['id']}
            movie_3.generate_website(user_movies, user_data)
        except KeyError:
            print(colored("Movie",'red'), colored(new_name,'green'),
                colored("not found",'red'))
        except TypeError:
            pass


def cmd_del_movie(user_movies, user_data):
    """ This function deletes a movie from the movies database and saves changes."""
    while True:
        movie_to_delete = input("Enter movie name to delete: ")
        if movie_to_delete in user_movies:
            storage.delete_movie(movie_to_delete, user_id=user_data['id'])
            print(colored("Movie",'blue'), colored(movie_to_delete,'green'),
                   colored("successfully deleted",'blue'))
            movies = storage.list_movies()
            user_movies = {title: info for title, info in movies.items()
                       if info.get('user_id') == user_data['id']}
            movie_3.generate_website(user_movies, user_data)
            break
        else:
            print(colored("Movie",'red',attrs=['bold']), colored(movie_to_delete,'green'),
                   colored("doesn't exist!",'red', attrs=['bold']))
            ask_again = input("Do you want to delete another one? (y/n): ")
            if ask_again.lower() != "y":
                break


def cmd_update_movie(user_movies, user_data):
    """ update movie """
    while True:
        movie_to_update = input("Enter movie name to update: ")
        if movie_to_update in user_movies:
            movie_note = input("Enter movie note: ")
            storage.update_movie(movie_to_update, movie_note, user_id=user_data['id'])
            print(colored("Movie",'blue'), colored(movie_to_update,'green'),
                  colored("successfully updated",'blue'))

            movies = storage.list_movies()
            user_movies = {title: info for title, info in movies.items()
                       if info.get('user_id') == user_data['id']}
            movie_3.generate_website(user_movies, user_data)
            break
        else:
            print(colored("Movie",'red',attrs=['bold']), colored(movie_to_update,'green'),
                  colored("doesn't exist!",'red',attrs=['bold']))
            ask_again = input("Do you want to update another one? (y/n): ")
            if ask_again.lower() != "y":
                break