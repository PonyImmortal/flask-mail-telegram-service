import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)

load_dotenv('config.env')

required_env_vars = ['SMTP_SERVER', 'SMTP_PORT', 'SMTP_USERNAME', 'SMTP_PASSWORD', 'SENDER_EMAIL', 'RECIPIENT_EMAIL',
                     'EMAIL_SUBJECT']

for var in required_env_vars:
    if not os.getenv(var):
        raise ValueError(f"Environment variable {var} is not set.")

smtp_server = os.getenv('SMTP_SERVER')
smtp_port = int(os.getenv('SMTP_PORT'))
smtp_username = os.getenv('SMTP_USERNAME')
smtp_password = os.getenv('SMTP_PASSWORD')


def send_email(name, email, message):
    sender_email = os.getenv('SENDER_EMAIL')
    recipient_email = os.getenv('RECIPIENT_EMAIL')
    subject = os.getenv('EMAIL_SUBJECT')

    message_body = f'Имя: {name}\nЭлектронная почта: {email}\nСообщение: {message}'

    mime_message = MIMEText(message_body)
    mime_message['From'] = sender_email
    mime_message['To'] = recipient_email
    mime_message['Subject'] = subject

    with smtplib.SMTP_SSL(smtp_server, smtp_port) as smtp:
        try:
            smtp.ehlo()
            smtp.login(smtp_username, smtp_password)
            smtp.send_message(mime_message)
            logging.info('Соединение с сервером SMTP установлено. Сообщение успешно отправлено.')
        except smtplib.SMTPException as e:
            logging.error('Ошибка при отправке сообщения.')
            logging.debug(f'Detailed SMTP error: {e}')
        except Exception as ex:
            logging.error('Ошибка при установке соединения с сервером SMTP.')
            logging.debug(f'Detailed error: {ex}')
