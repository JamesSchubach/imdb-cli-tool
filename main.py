from bs4 import BeautifulSoup
from requests import get

"""
"""


def getResponse(base, query):
    return get(base+query)


def reverseList(list, bool):
    return list[::-1] if not bool else list


base_url = 'https://www.imdb.com/'

print("IMDB Movie Star Search")
print("**********************")
# user_input = input("\nHello, Please enter the Movie Stars Name: ")
user_input = "Tom Cruise"

query = "find?q=" + user_input.replace(" ", "+") + '&s=nm'

response = getResponse(base_url, query)

# Parsing through the response data to grab a list of given actors for the actor name
soup = BeautifulSoup(response.text, 'html.parser')

results = soup.findAll("table", {"class": "findList"})[0]
actors = results.findAll("td", {"class": "result_text"})


# List comprehension which returns a list of tuples, in the form (Actor Name, URL for Actor)
actor_list = [(el[0].getText(), el[0]['href'])
              for actor in actors if (el := actor.findAll('a')) != 'NaN']

# Prints out the list of actors with a enumerated number
[print((str(i) + "."), actor[0]) for i, actor in enumerate(actor_list, 1)]
print("It seems your query has returned a couple of actors, which actor were you looking for? ")
user_input = input("Please enter the number next to the actor above: ")

# Checks or errors from user input, will continue to prompt user until they enter a valid number
while True:
    try:
        user_input = int(user_input)
        indx = user_input - 1
        break
    except ValueError as err:
        user_input = input("Please enter a valid number listed above: ")

actor_name = actor_list[indx][0]
print("Awesome, I will now list the movies %s is in" % actor_name)
user_input = input(
    "By the way, would you like the movies listed in newest first? [y/n]: ")

if user_input == "y":
    reverse = True
else:
    reverse = False

query = actor_list[indx][1]
response = getResponse(base_url, query)

# Once again parses through the given response, returning all the films given actor is in
soup = BeautifulSoup(response.text, 'html.parser')
results = soup.findAll("div", {"class": "filmo-category-section"})[0]
results = results.findAll("b")

print("\nThe movies that %s is in are:" % actor_name)

# Prints the list of movies that the actor is in
[print(movie.getText()) for movie in reverseList(results, reverse)]
