import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

# Archivo CSV para escribir los resultados
current_date = datetime.now().strftime("%Y%m%d")
current_date_for_name = datetime.now().strftime("%Y%m%d%H%M%S")
csv_file = open('productosJD' + current_date_for_name + ".csv", 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Título', 'Enlace', 'Colores', 'Precio', 'Moneda', 'Fecha'])

# URLs de las páginas para scrapear
pages = ['https://www.jdsports.es/hombre/ropa-de-hombre/latest/',
         'https://www.jdsports.es/hombre/calzado-de-hombre/zapatillas/'
        ]
nurls = 0
for page in pages:
    soup = BeautifulSoup(requests.get(page).content, 'html.parser') # obtener el contenido de la página
    product_items = soup.find_all(class_='productListItem') # obtener todos los productos mediante la etiqueta html de productos

    for product in product_items:
        product_title = product.find(class_='itemTitle').find('a').text # obtener el título de los productos
        product_price = product.find(class_='itemPrice').find(class_='pri').text # obtener el precio de los productos
        product_price = product_price.replace("€", "")
        product_price = product_price.replace(",", ".")
        product_link = "https://www.jdsports.es" + product.find(class_='itemTitle').find('a')['href']  # obtener el enlace de los productos

        # Busca y muestra los colores disponibles
        colors = []
        try:
            productSoup = BeautifulSoup(requests.get(product_link).content, 'html.parser') # obtener el contenido de la página
            color_list = productSoup.find('ul', class_='smScroll').find_all('li')
            for color in color_list:
                img = color.find('img')
                if img:
                    color_name = img['title']
                    colors.append(color_name)
        except Exception as e:
            colors.append('Nan') # Si no hay colores, agrega 'Nan' a la lista

        # Si hay colores, formatea la cadena de colores
        if colors:
            if len(colors) > 1:
                color_string = ', '.join(colors[:-1]) + colors[-1]
            else:
                color_string = colors[0]
    
        # Escribe los resultados en el archivo CSV
        csv_writer.writerow([product_title, product_link, color_string, product_price, "€", current_date])
        nurls += 1
print("Listo! Se han generado", nurls, "filas")
csv_file.close()
