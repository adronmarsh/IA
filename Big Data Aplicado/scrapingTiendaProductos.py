import requests
from bs4 import BeautifulSoup

page = requests.get("https://www.temu.com/es/electronica-o3-248.html")

soup = BeautifulSoup(page.content)
# print(soup.prettify)
