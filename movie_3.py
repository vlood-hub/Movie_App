""" Ready for movie night? This program offers a playlist worth exploring
             — dive in and discover its cool features! """

import random
import sys
import matplotlib.pyplot as plt
import countryflag
from termcolor import colored
from statistics import median
from db_manager import movie_storage_sql as storage
from api import data_fetcher
from CRUD import crud_movie, crud_user

READ_HTML_FILE = 'templates/index_template.html'


def stats(user_movies):
    """ analytics """
    ratings = [float(attributes['rating']) for attributes in user_movies.values()]

    #   average rating
    print(colored(f"Average rating: {sum(ratings)/len(user_movies):.2f}",'yellow'))

    #   median rating
    print(colored(f"Median rating: {median(ratings):.2f}",'yellow'))

    #   best movie(s)
    best_rating = max(float(m["rating"]) for m in user_movies.values())

    best_movies = [title for title, attrs in user_movies.items()
                if float(attrs["rating"]) == best_rating]

    print(colored(f"Best movie(s): {', '.join(best_movies)}, {best_rating}", 'yellow'))

    #  worst movie(s)
    worst_rating = min(float(m["rating"]) for m in user_movies.values())

    worst_movies = [title for title, attrs in user_movies.items()
                if float(attrs["rating"]) == worst_rating]

    print(colored(f"Worst movie(s): {', '.join(worst_movies)}, {worst_rating}", 'yellow'))


def random_movie(user_movies):
    """ random movie choice """
    name, attributes = random.choice(list(user_movies.items()))
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


def search_movie(user_movies):
    """ search movie """
    while True:
        user_input = input("Enter part of movie name: ")
        found = False

        for name, attributes in user_movies.items():
            if user_input.lower() in name.lower():
                print(f"{name} ({attributes['year']}), {attributes['rating']}")
                found = True

        if found:
            break

        similar = []
        for name in user_movies:
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


def sort_movie(user_movies):
    """ This function sorts movies by their rating or lists them in chronological order. """
    while True:
        try:
            user_choice = int(input("Should the movies be sorted by rating or by release year? " \
                                    "1 - rating / 2 - year: "))

            # """ sort movie list highest rating first """
            if user_choice == 1:
                sorted_movies = sorted(user_movies.items(),
                                key=lambda item: float(item[1]['rating']),
                                reverse=True)
                break

            # """ sort movies by release year """
            elif user_choice == 2:
                while True:
                    latest_movie = input("Do you want to see the latest movies first or last? ")
                    if latest_movie == "first":
                        sorted_movies = sorted(user_movies.items(),
                                        key=lambda item: int(item[1]['year']),
                                        reverse=True)
                        break
                    elif latest_movie == "last":
                        sorted_movies = sorted(user_movies.items(),
                                        key=lambda item: int(item[1]['year']))
                        break
                    else:
                        print("Please type first or last. Any other input is invallid")
                break
            else:
                print("Please enter 1 or 2. Any other input is invallid")

        except ValueError:
            print("Please enter 1 or 2. Any other input is invallid")

    print(f"\n{len(sorted_movies)} movies in total\n")
    print(f"{'Title (release year)':<50} Rating\n")
    for name, attributes in sorted_movies:
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


def serialize_movie(title, info, imdb, flag):
    """ Serializes movie data """
    output = ''
    output += '<li>'
    output += '<div class="movie">'
    output += '<div class="container">'
    output += f'<a href="https://www.imdb.com/title/{imdb}">'
    output += f'<img class="movie-poster" src={info["poster"]} title="{info["note"]}">'
    output += '</a>'
    output += '<div class="flag">'
    output += f'<span><strong>{flag}</strong></span>'
    output += '</div>'
    output += '<div class="ratinginfo">'
    output += f'<span><strong>{info["rating"]}</strong></span>'
    output += '</div>'
    output += '</div>'
    output += f'<div class="movie-title">{title}</div>'
    output += f'<div class="movie-year">{info["year"]}</div>'
    output += '</div>'
    output += '</li>'

    return output


def generate_website(user_movies, user_data):
    """ geberate website with a movie list """
    WRITE_NEW_HTML_FILE = f'{user_data['name']}.html'
    orig_html_file = read_write_file(READ_HTML_FILE, 'read')
    output = ''
    #print(user_movies)

    for title, info in user_movies.items():
        movie = data_fetcher.fetch_data(title)
        country = str(movie["Country"].split(',')[0])
        flag = countryflag.getflag(country)
        imdb = movie["imdbID"]
        output += serialize_movie(title, info, imdb, flag)

    template_title = f'{user_data['name']}\'s Movie App'
    new_html_file = orig_html_file.replace('__TEMPLATE_TITLE__', template_title).replace(
        '__TEMPLATE_MOVIE_GRID__', output)
    read_write_file(WRITE_NEW_HTML_FILE, 'write', new_html_file)
    print(colored("Website was successfully generated or updated to the file",'blue'),
          colored(WRITE_NEW_HTML_FILE,'green'))


def filter_movies(user_movies):
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
    for name, attributes in user_movies.items()
    if (min_rating is None or float(attributes['rating']) >= min_rating)
    and (start_year is None or int(attributes['year']) >= start_year)
    and (end_year is None or int(attributes['year']) <= end_year)
    }

    print(f"\n{len(filtered_movies)} movies in total\n")
    print(f"{'Title (year)':<50} Rating\n")
    for name, attributes in filtered_movies.items():
        left = f"{name} ({attributes['year']})"
        print(f"{left:<51}: {attributes['rating']}")


def rating_histogram(user_movies):
    """ rating histogram """
    ratings = [movie["rating"] for movie in user_movies.values()]
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


def movies_cmd(user_data):
    """ menu """
    print(colored(f"\n********** {user_data['name']}'s Movies Database **********\n",
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
        99. Switch user\n
                      """, 'magenta'))

        movies = storage.list_movies()
        user_movies = {title: info for (user_id, title), info in movies.items()
            if user_id == user_data['id']}
        try:
            user_choice = int(input("Enter choice 1-10: "))
            print()

            match user_choice:
                case 0: print(f"Bye {user_data['name']}!"); sys.exit()
                case 1: crud_movie.cmd_list_movies(user_movies,user_data)
                case 2: crud_movie.cmd_add_movie(user_movies,user_data)
                case 3: crud_movie.cmd_del_movie(user_movies,user_data)
                case 4: crud_movie.cmd_update_movie(user_movies,user_data)
                case 5: stats(user_movies)
                case 6: random_movie(user_movies)
                case 7: search_movie(user_movies)
                case 8: sort_movie(user_movies)
                case 9: generate_website(user_movies,user_data)
                case 10: filter_movies(user_movies)
                case 11: rating_histogram(user_movies)
                case 99: crud_user.cmd_users_list()

        except ValueError:
            print("Enter a number (see menu)")

        input("\nPress enter to continue")


def main():
    """ In the beginning was the main() """
    print("\nWelcome to the Movie App! 🎬\n")
    crud_user.cmd_users_list()


if __name__ == "__main__":
    main()