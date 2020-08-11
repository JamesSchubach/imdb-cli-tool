from bs4 import BeautifulSoup
from requests import get

base_url = 'https://www.imdb.com/find?'

print("IMDB Movie Star Search")
print("**********************")
# name = input("\nHello, Please enter the Movie Stars Name: ")
name = "Tom Cruise"

query = "q=" + name.replace(" ", "+")
print(query)

print(base_url+query)
response = get(base_url+query)
# print(response.text)

soup = BeautifulSoup("response.text")
