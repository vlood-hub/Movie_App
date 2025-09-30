""" Ready for movie night? This program offers a playlist worth exploring
             — dive in and discover its cool features! """

import random
import matplotlib.pyplot as plt
from termcolor import colored
from statistics import median
from db_manager import movie_storage_sql as storage
from api import data_fetcher

READ_HTML_FILE = 'templates/index_template.html'
WRITE_NEW_HTML_FILE = 'index.html'


def cmd_list_movies(movies):
    """ Retrieve and display all movies from the database. """
    print(f"{len(movies)} movies in total\n")
    print(f"{'Title (year)':<50} Rating\n")

    for name, attributes in movies.items():
        left = f"{name} ({attributes['year']})"
        print(f"{left:<51}: {attributes['rating']}")


def cmd_add_movie(movies):
    """ The function adds a movie to the movies database and saves changes. """
    while True:
        new_name = input("Enter new movie name: ")
        if new_name == "":
            print("Empty input")
        else:
            break
    if new_name in movies:
        print(colored("Movie",'red'), colored(new_name,'green'),
            colored("already exists", 'red'))
    else:
        try:
            movie = data_fetcher.fetch_data(new_name)
            storage.add_movie(movie['Title'], movie['Year'], movie['imdbRating'], movie['Poster'])
            print(colored("Movie",'blue'), colored(movie['Title'],'green'),
                colored("successfully added",'blue'))
        except KeyError:
            print(colored("Movie",'red'), colored(new_name,'green'),
                colored("not found", 'red'))
        except TypeError:
            pass


def cmd_del_movie(movies):
    """ This function deletes a movie from the movies database and saves changes."""
    while True:
        movie_to_delete = input("Enter movie name to delete: ")
        if movie_to_delete in movies:
            storage.delete_movie(movie_to_delete)
            print(colored("Movie",'blue'), colored(movie_to_delete,'green'),
                   colored("successfully deleted",'blue'))
            break
        else:
            print(colored("Movie",'red',attrs=['bold']), colored(movie_to_delete,'green'),
                   colored("doesn't exist!",'red', attrs=['bold']))
            ask_again = input("Do you want to delete another one? (y/n): ")
            if ask_again.lower() != "y":
                break


def cmd_update_movie(movies, movie_to_update = ""):
    """ update movie """
    while True:
        if movie_to_update == "":
            movie_to_update = input("Enter movie name to update: ")
        if movie_to_update in movies:
            new_rating = float(input("Enter new movie rating (0-10): "))
            storage.update_movie(movie_to_update, new_rating)
            print(colored("Movie",'blue'), colored(movie_to_update,'green'),
                  colored("successfully updated",'blue'))
            break
        else:
            print(colored("Movie",'red',attrs=['bold']), colored(movie_to_update,'green'),
                  colored("doesn't exist!",'red',attrs=['bold']))
            ask_again = input("Do you want to update another one? (y/n): ")
            movie_to_update = ""
            if ask_again.lower() != "y":
                break


def stats(movies):
    """ analytics """
    ratings = [float(attributes['rating']) for attributes in movies.values()]

    #   average rating
    print(colored(f"Average rating: {sum(ratings)/len(movies):.2f}",'yellow'))

    #   median rating
    print(colored(f"Median rating: {median(ratings):.2f}",'yellow'))

    #   best movie(s)
    best_rating = max(float(m["rating"]) for m in movies.values())

    best_movies = [title for title, attrs in movies.items()
                if float(attrs["rating"]) == best_rating]

    print(colored(f"Best movie(s): {', '.join(best_movies)}, {best_rating}", 'yellow'))

    #  worst movie(s)
    worst_rating = min(float(m["rating"]) for m in movies.values())

    worst_movies = [title for title, attrs in movies.items()
                if float(attrs["rating"]) == worst_rating]

    print(colored(f"Worst movie(s): {', '.join(worst_movies)}, {worst_rating}", 'yellow'))


def random_movie(movies):
    """ random movie choice """
    name, attributes = random.choice(list(movies.items()))
    print(f"Your movie for tonight {colored(name, 'blue')} "
        f"({colored(attributes['year'], 'blue')}), "
        f"it's rated {colored(attributes['rating'], 'blue')}")


def edit_distance(user_input, name):
    """ Levenshtein Distance Function """
    m, n = len(user_input), len(name)
    dist = [[0]*(n+1) for _ in range(m+1)]

    for i in range(m+1):
        for j in range(n+1):
            if i == 0: dist[i][j] = j
            elif j == 0: dist[i][j] = i
            elif user_input[i-1] == name[j-1]:
                dist[i][j] = dist[i-1][j-1]
            else:
                dist[i][j] = 1 + min(
                    dist[i-1][j],    # Delete
                    dist[i][j-1],    # Insert
                    dist[i-1][j-1]   # Replace
                )
    return dist[m][n]


def search_movie(movies):
    """ search movie """
    while True:
        user_input = input("Enter part of movie name: ")
        found = False

        for name, attributes in movies.items():
            if user_input.lower() in name.lower():
                print(f"{name} ({attributes['year']}), {attributes['rating']}")
                found = True

        if found:
            break

        similar = []
        for name in movies:
            distance = edit_distance(user_input.lower(), name.lower())
            if distance <= 7:  # Threshold for similarity
                similar.append(name)

        if similar:
            print(f"The movie {colored(user_input,'green')} does not exist. Did you mean:")
            for name in similar:
                print(colored(name,'blue'))
        else:
            print(colored("Movie not found and no similar matches",'red', attrs=['bold']))
            ask_again = input("Would you like to try another search? (y/n): ")
            if ask_again.lower() != "y":
                break


def sort_movie(movies):
    """ This function sorts movies by their rating or lists them in chronological order. """
    while True:
        try:
            user_choice = int(input("Should the movies be sorted by rating or by release year? " \
                                    "1 - rating / 2 - year: "))

            # """ sort movie list highest rating first """
            if user_choice == 1:
                movies = sorted(movies.items(),
                                key=lambda item: float(item[1]['rating']),
                                reverse=True)
                break

            # """ sort movies by release year """
            elif user_choice == 2:
                while True:
                    latest_movie = input("Do you want to see the latest movies first or last? ")
                    if latest_movie == "first":
                        movies = sorted(movies.items(),
                                        key=lambda item: int(item[1]['year']),
                                        reverse=True)
                        break
                    elif latest_movie == "last":
                        movies = sorted(movies.items(),
                                        key=lambda item: int(item[1]['year']))
                        break
                    else:
                        print("Please type first or last. Any other input is invallid")
                break
            else:
                print("Please enter 1 or 2. Any other input is invallid")

        except ValueError:
            print("Please enter 1 or 2. Any other input is invallid")

    print(f"\n{len(movies)} movies in total\n")
    print(f"{'Title (release year)':<50} Rating\n")
    for name, attributes in movies:
        left = f"{name} ({attributes['year']})"
        print(f"{left:<51}: {attributes['rating']}")


def read_write_file(file_path, attr, obj=''):
    """ Read and writes html files """
    if attr == 'read':
        with open(file_path, "r", encoding="utf8") as file_in:
            orig_html_file = file_in.read()
            return orig_html_file
    elif attr == 'write':
        with open(file_path, "w", encoding="utf8") as file_out:
            file_out.write(obj)


def serialize_movie(title, info):
    """ Serializes movie data """
    output = ''
    output += '<li>'
    output += '<div class="movie">'
    output += f'<img class="movie-poster" src={info["poster"]} title="">'
    output += f'<div class="movie-title">{title}</div>'
    output += f'<div class="movie-year">{info["year"]}</div>'

    # try:
    #     output += f'<li><strong>Type:</strong> {animal_data["characteristics"]["type"]}</li>'
    #     output += f'<li><strong>Group:</strong> {animal_data["characteristics"]["group"]}</li>'
    # except KeyError:
    #     pass

    output += '</div>'
    output += '</li>'

    return output


def generate_website(movies):
    """ """
    orig_html_file = read_write_file(READ_HTML_FILE, 'read')

    output = ''
    for title, info in movies.items():
        output += serialize_movie(title, info)

    new_html_file = orig_html_file.replace('__TEMPLATE_TITLE__', 'My Movie App').replace('__TEMPLATE_MOVIE_GRID__', output)
    read_write_file(WRITE_NEW_HTML_FILE, 'write', new_html_file)
    print(f"Website was successfully generated to the file {WRITE_NEW_HTML_FILE}")

def filter_movies(movies):
    """ This function filters a list of movies based on specific criteria such as
                minimum rating, start year, and end year. """
    while True:
        min_rating = input("Enter minimum rating (leave blank for no minimum rating): ")
        start_year = input("Enter start year (leave blank for no start year): ")
        end_year = input("Enter end year (leave blank for no end year): ")

        try:
            min_rating = float(min_rating) if min_rating else None
            start_year = int(start_year) if start_year else None
            end_year = int(end_year) if end_year else None
            break
        except ValueError:
            print(colored(
                "Rating must be a number (decimals allowed), years must be integers. Try again!\n",
                'red'))


    filtered_movies = {
    name: attributes
    for name, attributes in movies.items()
    if (min_rating is None or float(attributes['rating']) >= min_rating)
    and (start_year is None or int(attributes['year']) >= start_year)
    and (end_year is None or int(attributes['year']) <= end_year)
    }

    print(f"\n{len(filtered_movies)} movies in total\n")
    print(f"{'Title (year)':<50} Rating\n")
    for name, attributes in filtered_movies.items():
        left = f"{name} ({attributes['year']})"
        print(f"{left:<51}: {attributes['rating']}")


def rating_histogram(movies):
    """ rating histogram """
    ratings = [movie["rating"] for movie in movies.values()]
    #   Plotting a rating histogram
    plt.hist(ratings, bins=10, color='skyblue', edgecolor='black')

    #   Adding labels and title
    plt.xlabel('Rating')
    plt.ylabel('Frequency')
    plt.title('Rating Histogram')

    #   Display the plot
    plt.show(block=False)

    #   Save the plot
    save_file()

    #   Close the plot
    plt.close()


def save_file():
    """ Save histogram plot to file """
    savehist = input("Do you want to save the plotted figure? (y/n): ")
    if savehist == "y":
        filename = input("Enter filename (.png or .pdf): ")
        plt.savefig(filename)

    print(colored("Figure was successfully saved",'blue'))


def menu():
    """ menu """
    print(colored("\n********** My Movies Database **********\n",
                  'cyan', attrs=['bold', 'underline']))

    while True:
        print(colored("""
        Menu:
        0.  Exit
        1.  List movies
        2.  Add movie
        3.  Delete movie
        4.  Update movie
        5.  Stats
        6.  Random movie
        7.  Search movie
        8.  Movies sorted by rating or chronologicaly
        9.  Generate webste
        10. Filter movies
        11. Create Rating Histogram\n
                      """, 'magenta'))

        movies = storage.list_movies()
        try:
            user_choice = int(input("Enter choice 1-10: "))
            print()

            match user_choice:
                case 0: print("Bye!"); break
                case 1: cmd_list_movies(movies)
                case 2: cmd_add_movie(movies)
                case 3: cmd_del_movie(movies)
                case 4: cmd_update_movie(movies)
                case 5: stats(movies)
                case 6: random_movie(movies)
                case 7: search_movie(movies)
                case 8: sort_movie(movies)
                case 9: generate_website(movies)
                case 10: filter_movies(movies)
                case 11: rating_histogram(movies)

        except ValueError:
            print("Enter a number (see menu)")

        input("\nPress enter to continue")


def main():
    """ This function calls menu with possible commands. """
    menu()


if __name__ == "__main__":
    main()