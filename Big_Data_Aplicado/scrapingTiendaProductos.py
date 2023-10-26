import requests
from bs4 import BeautifulSoup

page = requests.get("https://mcdonalds.es/api/sitemap.xml")

soup = BeautifulSoup(page.content)
# print(soup.prettify)
