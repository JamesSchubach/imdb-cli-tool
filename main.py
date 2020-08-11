from bs4 import BeautifulSoup
from requests import get

base_url = 'https://www.imdb.com/'

print("IMDB Movie Star Search")
print("**********************")
# user_input = input("\nHello, Please enter the Movie Stars Name: ")
user_input = "Tom Cruise"

query = "find?q=" + user_input.replace(" ", "+") + '&s=nm'
# print(query)

# print(base_url+query)
response = get(base_url+query)
# print(response.text)

soup = BeautifulSoup(response.text, 'html.parser')

results = soup.findAll("table", {"class": "findList"})[0]
actors = results.findAll("td", {"class": "result_text"})

actor_list = [(el[0].getText(), el[0]['href'])
              for actor in actors if (el := actor.findAll('a')) != 'NaN']

[print((str(i) + "."), actor[0]) for i, actor in enumerate(actor_list, 1)]
print("It seems your query has returned a couple of actors, which actor were you looking for? ")
user_input = input("Please enter the number next to the actor above: ")

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

query = actor_list[indx][1]
response = get(base_url+query)

soup = BeautifulSoup(response.text, 'html.parser')
results = soup.findAll("div", {"class": "filmo-category-section"})[0]
results = results.findAll("b")

print("\nThe movies that %s is in are:" % actor_name)
[print(results[x].getText()) for x in range(len(results)-1, -1, -1)]
