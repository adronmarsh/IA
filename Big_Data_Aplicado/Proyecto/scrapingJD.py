import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import yaml
from confluent_kafka import Producer 
import socket
import json

def kafka(producto_kafka):

    conf = {'bootstrap.servers': 'localhost:9092',  # Configurar la dirección del servidor Kafka
            'client.id': socket.gethostname()}  # Configurar el ID del cliente como el nombre del host

    producer = Producer(conf)  # Crear una instancia de la clase Producer con la configuración proporcionada

    def acked(err, msg):
        """
        Función de callback para manejar el resultado de la entrega del mensaje.

        Parameters:
        - err: Objeto de error, None si la entrega fue exitosa.
        - msg: Objeto de mensaje que contiene información sobre el mensaje producido.
        """
        if err is not None:
            print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
        else:
            print("Message produced: %s" % (str(msg)))


    # Enviar cada elemento del JSON como un mensaje Kafka
    for item in producto_kafka:
        # Convierte el diccionario a una cadena JSON antes de enviarlo
        json_string = json.dumps(item)
        producer.produce('kakfaJD', key="key", value=str(json_string), callback=acked)
        producer.poll(1)  # Permitir que el productor realice cualquier trabajo pendiente durante 1 milisegundo

    # Esperar a que todos los mensajes se envíen antes de salir
    producer.flush()


# Carga las credenciales desde el archivo YAML
with open('/home/aibg/IA/Big_Data_Aplicado/Proyecto/credentials.yaml', 'r') as file:
# with open('credentials.yaml', 'r') as file:
    credentials = yaml.safe_load(file)

# Configuración de la cuenta de correo
email_address = credentials['email_address']
email_password = credentials['email_password']
receiver_email = credentials['receiver_email']
smtp_server = credentials['smtp_server']
smtp_port = credentials['smtp_port']

# Archivo CSV para escribir los resultados
current_date = datetime.now().strftime("%Y%m%d")
current_date_for_name = datetime.now().strftime("%Y%m%d%H%M%S")
csv_file = open('/home/aibg/IA/Big_Data_Aplicado/Proyecto/results/productosJD' + current_date_for_name + ".csv", 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Título', 'Enlace', 'Colores', 'Precio', 'Moneda', 'Fecha'])

# URLs de las páginas para scrapear
pages = ['https://www.jdsports.es/hombre/ropa-de-hombre/latest/',
         'https://www.jdsports.es/hombre/calzado-de-hombre/zapatillas/'
        ]
nurls = 0
producto_kafka_list = []  # Lista para almacenar los datos que se enviarán a Kafka
for page in pages:
    soup = BeautifulSoup(requests.get(page).content, 'html.parser') # Obtener el contenido de la página
    product_items = soup.find_all(class_='productListItem') # Obtener todos los productos mediante la etiqueta html de productos

    for product in product_items:
        product_title = product.find(class_='itemTitle').find('a').text # Obtener el título de los productos
        product_price = product.find(class_='itemPrice').find(class_='pri').text # Obtener el precio de los productos
        product_price = product_price.replace("€", "")
        product_price = product_price.replace(",", ".")
        product_link = "https://www.jdsports.es" + product.find(class_='itemTitle').find('a')['href']  # Obtener el enlace de los productos
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
            colors.append('None') # Si no hay colores, agrega 'None' a la lista

        # Si hay colores, formatea la cadena de colores
        if colors:
            if len(colors) > 1:
                color_string = ', '.join(colors[:-1]) + colors[-1]
            else:
                color_string = colors[0]
    
        # Añadir los datos a la lista
        producto_kafka_list.append({
            'Título': product_title,
            'Enlace': product_link,
            'Colores': color_string,
            'Precio': product_price,
            'Moneda': '€',
            'Fecha': current_date
        })
        
        # Escribe los resultados en el archivo CSV
        csv_writer.writerow([product_title, product_link, color_string, product_price, "€", current_date])
        
        # Envía los datos al servidor Kafka
        kafka(producto_kafka_list)
        nurls += 1
        
print("Listo! Se han generado", nurls, "filas")
csv_file.close()

csv_file_path = '/home/aibg/IA/Big_Data_Aplicado/Proyecto/results/productosJD' + current_date_for_name + ".csv"
json_file_path = '/home/aibg/IA/Big_Data_Aplicado/Proyecto/results/productosJD' + current_date_for_name + ".json"


# # Envía un correo electrónico con el número de filas generadas
# subject = "Número de filas generadas"
# message = f"Se han generado {nurls} filas al ejecutar el código."
# msg = MIMEMultipart()
# msg['From'] = email_address
# msg['To'] = receiver_email
# msg['Subject'] = subject
# msg.attach(MIMEText(message, 'plain'))

# # Adjunta el archivo CSV al correo
# with open(csv_file_path, "rb") as file:
#     part = MIMEApplication(file.read(), Name=f"productosJD{current_date_for_name}.csv")
#     part['Content-Disposition'] = f'attachment; filename="productosJD{current_date_for_name}.csv"'
#     msg.attach(part)

# try:
#     server = smtplib.SMTP(smtp_server, smtp_port)
#     server.starttls()
#     server.login(email_address, email_password)
#     server.sendmail(email_address, receiver_email, msg.as_string())
#     server.quit()
#     print("Correo enviado con éxito")
# except Exception as e:
#     print(f"No se pudo enviar el correo: {str(e)}")