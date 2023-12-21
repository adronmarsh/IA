import os
import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import socket
import json
import yaml
import smtplib
from confluent_kafka import Producer
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def kafka(producto_kafka, producer):
    for item in producto_kafka:
        json_string = json.dumps(item)
        producer.produce('kafkaJD', key="key", value=str(json_string), callback=acked)
        producer.poll(1)

    producer.flush()

def acked(err, msg):
    if err is not None:
        print(f"Failed to deliver message: {msg}: {err}")
    else:
        print(f"Message produced: {msg}")

def scrape_colors(product_link):
    try:
        product_soup = BeautifulSoup(requests.get(product_link).content, 'html.parser')
        color_list = product_soup.find('ul', class_='smScroll').find_all('li')
        return [img['title'] for color in color_list if (img := color.find('img'))]
    except Exception as e:
        return ['None']

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    credentials_path = os.path.join(script_dir, 'credentials.yaml')

    with open(credentials_path, 'r') as file:
        credentials = yaml.safe_load(file)

    email_address = credentials['email_address']
    email_password = credentials['email_password']
    receiver_email = credentials['receiver_email']
    smtp_server = credentials['smtp_server']
    smtp_port = credentials['smtp_port']

    current_date = datetime.now().strftime("%Y%m%d")
    current_date_for_name = datetime.now().strftime("%Y%m%d%H%M%S")
    csv_file_path = os.path.join(script_dir, 'results', f'productosJD{current_date_for_name}.csv')

    conf = {'bootstrap.servers': 'localhost:9092',
            'client.id': socket.gethostname()}

    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Título', 'Enlace', 'Colores', 'Precio', 'Moneda', 'Fecha'])

        pages = ['https://www.jdsports.es/hombre/ropa-de-hombre/latest/',
                 'https://www.jdsports.es/hombre/calzado-de-hombre/zapatillas/']

        nurls = 0

        for page in pages:
            soup = BeautifulSoup(requests.get(page).content, 'html.parser')
            product_items = soup.find_all(class_='productListItem')

            for product in product_items:
                product_title = product.find(class_='itemTitle').find('a').text
                product_price = product.find(class_='itemPrice').find(class_='pri').text.replace("€", "").replace(",", ".")
                product_link = "https://www.jdsports.es" + product.find(class_='itemTitle').find('a')['href']
                colors = scrape_colors(product_link)

                color_string = ', '.join(colors) if colors else 'None'
                
                individual_producer = Producer(conf)

                kafka([{
                    'Título': product_title,
                    'Enlace': product_link,
                    'Colores': color_string,
                    'Precio': product_price,
                    'Moneda': '€',
                    'Fecha': current_date
                }], individual_producer)

                csv_writer.writerow([product_title, product_link, color_string, product_price, "€", current_date])
                nurls += 1

    print(f"Listo! Se han generado {nurls} filas")

    subject = "Número de filas generadas"
    message = f"Se han generado {nurls} filas al ejecutar el código."
    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    with open(csv_file_path, "rb") as file:
        part = MIMEApplication(file.read(), Name=f"productosJD{current_date_for_name}.csv")
        part['Content-Disposition'] = f'attachment; filename="productosJD{current_date_for_name}.csv"'
        msg.attach(part)

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_address, email_password)
        server.sendmail(email_address, receiver_email, msg.as_string())
        server.quit()
        print("Correo enviado con éxito")
    except Exception as e:
        print(f"No se pudo enviar el correo: {str(e)}")

if __name__ == "__main__":
    main()
