import requests
from bs4 import BeautifulSoup

import csv

# Realizar una solicitud HTTP GET a la página web
page = requests.get('https://www.temu.com/es/electronica-o3-248.html')

# Crear un objeto BeautifulSoup con el contenido HTML de la página web
soup = BeautifulSoup(page.content, 'html.parser')

# Encontrar todos los elementos HTML que contienen información del producto
products = soup.find_all('div', class_='product-item')

print(page)
# print("Producto:", products)
# # Crear un archivo CSV para almacenar los datos del producto
# with open('productos.csv', mode='w', newline='') as file:
#     writer = csv.writer(file)

#     # Escribir encabezados de columna en el archivo CSV
#     writer.writerow(['Nombre', 'Precio'])

#     # Iterar sobre cada elemento HTML del producto y extraer información relevante
#     for product in products:
#         name = product.find('a', class_='product-title').text.strip()
#         price = product.find('span', class_='price').text.strip()

#         # Escribir información del producto en el archivo CSV
#         writer.writerow([name, price])