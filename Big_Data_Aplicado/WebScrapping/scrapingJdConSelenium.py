import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import csv
from datetime import datetime

# Configuración de ChromeDriver para Selenium
chrome_driver_path = r'C:\Users\Adri\Downloads\chromedriver-win64\chromedriver.exe'
chrome_service = ChromeService(executable_path=chrome_driver_path)
chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# Archivo CSV para escribir los resultados
current_date = datetime.now().strftime("%Y%m%d")
current_date_for_name = datetime.now().strftime("%Y%m%d%H%M%S")
csv_file = open('productosJD' + current_date_for_name + ".csv", 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Título', 'Enlace', 'Talla', 'Stock', 'Colores', 'Precio', 'Moneda', 'Fecha'])

# URLs de las páginas para scrapear
pages = ['https://www.jdsports.es/hombre/ropa-de-hombre/latest/',
         'https://www.jdsports.es/hombre/calzado-de-hombre/zapatillas/'
        ]

for page in pages:
    soup = BeautifulSoup(requests.get(page).content, 'html.parser') # Obtener el contenido de la página
    product_items = soup.find_all(class_='productListItem') # Obtener todos los productos mediante la etiqueta html de productos

    for product in product_items:
        product_title = product.find(class_='itemTitle').find('a').text # Obtener el título de los productos
        product_price = product.find(class_='itemPrice').find(class_='pri').text # Obtener el precio de los productos
        product_price = product_price.replace("€", "")
        product_price = product_price.replace(",", ".")
        product_link = "https://www.jdsports.es" + product.find(class_='itemTitle').find('a')['href'] # Obtener el enlace de los productos

        # Busca y muestra los colores disponibles
        colors = []
        try:
            productSoup = BeautifulSoup(requests.get(product_link).content, 'html.parser') # Obtener el contenido de la página
            color_list = productSoup.find('ul', class_='smScroll').find_all('li')
            for color in color_list:
                img = color.find('img')
                if img:
                    color_name = img['title']
                    colors.append(color_name)
        except Exception as e:
            colors.append('Nan') # Si no hay colores, agrega 'Nan' a la lista

        driver.get(product_link) # Abre la página de productos con Selenium

        size_buttons = driver.find_elements(By.CSS_SELECTOR, 'button[data-e2e="pdp-productDetails-size"]')
        for size_button in size_buttons:
            size = size_button.get_attribute('data-size')
            price = size_button.get_attribute('data-price')
            stock = size_button.get_attribute('data-stock')

            # Si hay colores, formatea la cadena de colores
            if colors:
                if len(colors) > 1:
                    color_string = ', '.join(colors[:-1]) + colors[-1]
                else:
                    color_string = colors[0]

            # Escribe los resultados en el archivo CSV
            csv_writer.writerow([product_title, product_link, size, stock, color_string, product_price, "€", current_date])

csv_file.close()
driver.quit()
