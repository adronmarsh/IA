import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import yaml
import os


def load_credentials():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    credentials_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'credentials.yaml')
    with open('credentials.yaml', 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def scrape_product_info(url):
    try:
        soup = BeautifulSoup(requests.get(url).content, 'html.parser')
        product_title = soup.find(class_='itemTitle').find('a').text
        product_price = soup.find(class_='itemPrice').find(class_='pri').text.replace("€", "").replace(",", ".")
        product_link = "https://www.jdsports.es" + soup.find(class_='itemTitle').find('a')['href']
        colors = [img['title'] for img in soup.find('ul', class_='smScroll').find_all('li', {'class': 'col'})]
        color_string = ', '.join(colors) if colors else 'None'
        return product_title, product_link, color_string, product_price
    except Exception as e:
        print(f"Error al obtener información del producto: {str(e)}")
        return None

def write_to_csv(file_path, data):
    with open(file_path, 'a', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(data)

def send_email(email_address, email_password, receiver_email, smtp_server, smtp_port, subject, message, file_path):
    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    with open(file_path, "rb") as file:
        part = MIMEApplication(file.read(), Name=os.path.basename(file_path))
        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
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

def main():
    credentials = load_credentials()

    email_address = credentials['email_address']
    email_password = credentials['email_password']
    receiver_email = credentials['receiver_email']
    smtp_server = credentials['smtp_server']
    smtp_port = credentials['smtp_port']

    current_date_for_name = datetime.now().strftime("%Y%m%d%H%M%S")
    csv_file_path = f'results/productosJD{current_date_for_name}.csv'

    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Título', 'Enlace', 'Colores', 'Precio', 'Moneda', 'Fecha'])

    pages = ['https://www.jdsports.es/hombre/ropa-de-hombre/latest/',
             'https://www.jdsports.es/hombre/calzado-de-hombre/zapatillas/']

    nurls = 0
    for page in pages:
        try:
            soup = BeautifulSoup(requests.get(page).content, 'html.parser')
            product_items = soup.find_all(class_='productListItem')

            for product in product_items:
                product_info = scrape_product_info("https://www.jdsports.es" + product.find(class_='itemTitle').find('a')['href'])
                if product_info:
                    data = [product_info[0], product_info[1], product_info[2], product_info[3], "€", datetime.now().strftime("%Y%m%d")]
                    write_to_csv(csv_file_path, data)
                    nurls += 1
        except Exception as e:
            print(f"Error al procesar la página {page}: {str(e)}")

    print(f"Listo! Se han generado {nurls} filas")

    subject = "Número de filas generadas"
    message = f"Se han generado {nurls} filas al ejecutar el código."
    send_email(email_address, email_password, receiver_email, smtp_server, smtp_port, subject, message, csv_file_path)

if __name__ == "__main__":
    main()
