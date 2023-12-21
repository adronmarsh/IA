# WebDataNotify Pipeline

WebDataNotify Pipeline es una solución integral para la recopilación de datos en tiempo real del sitio web de JD Sports, procesamiento de datos mediante técnicas de web scraping y notificación eficiente a través de correo electrónico utilizando Kafka como sistema de mensajería.

## Tabla de Contenidos

- [WebDataNotify Pipeline](#webdatanotify-pipeline)
  - [Tabla de Contenidos](#tabla-de-contenidos)
  - [Descripción General](#descripción-general)
  - [Funcionalidades](#funcionalidades)
  - [Requisitos](#requisitos)
  - [Instalación](#instalación)
  - [Uso](#uso)
  - [Configuración](#configuración)
  - [Licencia](#licencia)

## Descripción General

WebDataNotify Pipeline está diseñado para automatizar la monitorización de información de productos en JD Sports. Utiliza web scraping dinámico para extraer detalles clave del producto, emplea Kafka para una transmisión eficiente de datos e integra un sistema de notificación por correo electrónico para actualizaciones oportunas.

## Funcionalidades

- **Web Scraping Dinámico:** Utiliza BeautifulSoup para web scraping dinámico, extrayendo detalles del producto como título, enlace, colores disponibles, precio y enlaces específicos a las páginas de productos.

- **Kafka Data Streaming:** Implementa Apache Kafka para una transmisión eficiente de datos, transformando detalles del producto en formato JSON y enviándolos a un tema de Kafka para procesamiento distribuido.

- **Pipeline de Datos:** Construye un robusto pipeline de datos utilizando Kafka, asegurando una gestión efectiva del flujo de información desde el scraping hasta la notificación por correo electrónico.

- **Notificaciones por Correo Electrónico:** Desarrolla un sistema automatizado de notificación por correo electrónico. Después de la recopilación y procesamiento de datos, se genera un informe detallado en formato CSV y se envía como archivo adjunto en un correo electrónico. El correo incluye información sobre el número de filas generadas en el archivo.

- **Gestión de Credenciales:** Incorpora un sistema seguro de gestión de credenciales a través de archivos YAML, garantizando la confidencialidad de información crítica como direcciones de correo electrónico y contraseñas.

## Requisitos

- Tener un servidor Kafka en ejecución en localhost:9092
- Python 3.x
- Bibliotecas: requests, bs4 (BeautifulSoup), csv, datetime, socket, json, yaml, smtplib, confluent_kafka

## Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/adronmarsh/IA.git
   cd Projects/WebDataNotify-Pipeline
   ```

2. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

## Uso

1. Configura las credenciales en el archivo `credentials.yaml`.

2. Ejecuta el script:

   ```bash
   python web_data_notify.py
   ```

3. Supervisa la consola para obtener actualizaciones de progreso y verifica tu correo electrónico para el archivo CSV generado.

## Configuración

Actualiza el archivo `credentials.yaml` con tu dirección de correo electrónico, contraseña, correo electrónico del destinatario, servidor SMTP y puerto.

```yaml
email_address: tu_correo@example.com
email_password: tu_contraseña_de_correo
receiver_email: destinatario@example.com
smtp_server: smtp.example.com
smtp_port: 587
```

## Licencia

Este proyecto está bajo la [Licencia MIT](LICENSE).