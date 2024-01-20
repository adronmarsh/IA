# WebDataNotify Pipeline

WebDataNotify Pipeline is a comprehensive solution for real-time data collection from JD Sports website, data processing through web scraping techniques, and efficient notification via email using Kafka as a messaging system.

## Table of Contents

- [WebDataNotify Pipeline](#webdatanotify-pipeline)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Features](#features)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Usage](#usage)
  - [License](#license)

## Overview

WebDataNotify Pipeline is designed to automate the monitoring of product information on JD Sports. It employs dynamic web scraping to extract key product details, utilizes Kafka for efficient data streaming, and integrates an email notification system for timely updates.

## Features

- **Dynamic Web Scraping:** Utilizes BeautifulSoup for dynamic web scraping, extracting product details such as title, link, available colors, price, and specific links to product pages.

- **Kafka Data Streaming:** Implements Apache Kafka for efficient data streaming, transforming product details into JSON format and sending them to a Kafka topic for distributed processing.

- **Data Pipeline:** Builds a robust data pipeline using Kafka, ensuring effective management of information flow from scraping to email notification.

- **Email Notifications:** Develops an automated email notification system. After data collection and processing, a detailed report in CSV format is generated and sent as an attachment in an email. The email includes information about the number of rows generated in the file.

- **Credential Management:** Incorporates a secure credential management system through YAML files, ensuring the confidentiality of critical information such as email addresses and passwords.

## Requirements

- Have a Kafka server running on localhost:9092
- Python 3.x
- Libraries: requests, bs4 (BeautifulSoup), csv, datetime, socket, json, yaml, smtplib, confluent_kafka

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/adronmarsh/IA.git
   cd Projects/WebDataNotify-Pipeline
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Configure the credentials in the `credentials.yaml` file.

2. Run the script:

   ```bash
   python web_data_notify.py
   ```

3. Monitor the console for progress updates and check your email for the generated CSV file.

4. Run the createReport.py file to create a report with the results.
   
   ````bash
   python createReport.py
   ```

## Configuration

Update the `credentials.yaml` file with your email address, password, receiver's email, SMTP server, and port.

```yaml
email_address: your_email@example.com
email_password: your_email_password
receiver_email: receiver@example.com
smtp_server: smtp.example.com
smtp_port: 587
```

## License

This project is licensed under the [MIT License](LICENSE).