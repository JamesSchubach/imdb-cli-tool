from bs4 import BeautifulSoup
from requests import get
import json
import re

# Global variables for imdb and parser
base_url = 'https://www.imdb.com/'
parser = 'html.parser'
regex = "^[a-zA-Z]+(([\'\,\.\- ][a-zA-Z ])?[a-zA-Z]*)*$"


def getResponse(base, query):
    return get(base+query)


# Helper function that makes reversing cleaner
def reverseList(list, bool):
    return list[::-1] if not bool else list


# Simple function that gets actor name
def getActorName():
    while True:
        user_input = input("\nHello, Please enter the Movie Stars Name: ")
        # user_input = "Tom Cruise"
        if re.search(regex, user_input):
            break
        else:
            print("Please enter a valid name.")
    # return input("\nHello, Please enter the Movie Stars Name: ")
    return user_input


def getActors(actor_name):
    query = "find?q=" + actor_name.replace(" ", "+") + '&s=nm'

    response = getResponse(base_url, query)
    # Parsing through the response data to grab a list of given actors for the actor name
    soup = BeautifulSoup(response.text, parser)

    results = soup.findAll("table", {"class": "findList"})[0]
    actors = results.findAll("td", {"class": "result_text"})

    # List comprehension which returns a list of tuples, in the form (Actor Name, URL for Actor)
    # actor_list = [(el[0].getText(), el[0]['href'])
    #               for actor in actors if (el := actor.findAll('a')) != 'NaN']
    actor_list = []
    for actor in actors:
        el = actor.findAll('a')[0]
        actor_list.append((el.getText(), el['href']))

    return actor_list


def getSpecificActor(actor_list):
    # Prints out the list of actors with a enumerated number
    [print((str(i) + "."), actor[0]) for i, actor in enumerate(actor_list, 1)]
    print("It seems your query has returned a couple of actors, which actor were you looking for? ")

    # Checks or errors from user input, will continue to prompt user until they enter a valid number
    while True:
        user_input = input("Please enter the number next to the actor above: ")
        try:
            user_input = int(user_input)
            indx = user_input - 1
            if indx >= len(actor_list):
                raise ValueError()
            break
        except ValueError as err:
            user_input = print("Please enter a valid number listed above")

    return actor_list[indx]


def getMovies(actor, reverse):
    query = actor[1]
    response = getResponse(base_url, query)

    # Once again parses through the given response, returning all the films given actor is in
    soup = BeautifulSoup(response.text, parser)
    results = soup.findAll("div", {"id": re.compile('actor-.*')})
    movies = []
    for movie in results:
        movies.append(movie.findAll("b"))
    movie_list = {"name": actor_name,
                  "movies": []
                  }

    for movie in reverseList(movies, reverse):
        movie = movie[0].getText()
        movie_list["movies"].append(movie)
    return movie_list


def printMovies(movies):
    # Prints the list of movies that the actor is in
    [print(movie) for movie in movies["movies"]]


def sendToJson(actor_name, movie_list):
    with open(actor_name.replace(" ", "_") + '_movies.json', 'w',  encoding='utf-8') as f:
        json.dump(movie_list, f, ensure_ascii=False,
                  indent=4)


def handleYesNo(question):
    while True:
        user_input = input(
            question)
        if (user_input in ('yes', 'no', 'y', 'n')):
            return str2bool(user_input)
        else:
            print("That wasn't valid option, try again ...")


def str2bool(string):
    return string in ('yes', 'y')


if __name__ == "__main__":
    print("IMDB Movie Star Search")
    print("**********************")
    actor_name = getActorName()
    actors = getActors(actor_name)
    if len(actors) > 1:
        actor = getSpecificActor(actors)
    else:
        actor = actors[0]
    actor_name = actor[0]

    print("\nAwesome, I will now list the movies %s is in" % actor_name)
    question = "By the way, would you like the movies listed in newest first? [y/n]: "
    user_input = handleYesNo(question)

    movies = getMovies(actor, user_input)
    print("\nThe movies that %s is in are:" % actor_name)
    printMovies(movies)
    question = "Would you like these movies published to a JSON document? [y/n]: "
    user_input = handleYesNo(question)
    if user_input:
        sendToJson(actor_name, movies)
