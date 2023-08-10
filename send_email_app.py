import logging
from flask import Flask, request, jsonify
from smtp_emailer import send_email
from flask_cors import CORS
from celery import Celery
from telegram_sendler import send_message_to_telegram

logging.basicConfig(level=logging.INFO)

celery_app = Celery('send_email_app.py', broker='redis://redis:6379/0')

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://example.ru"}})


@celery_app.task
def send_telegram_message_task(name, email, message):
    try:
        send_message_to_telegram(name, email, message)
    except Exception as e:
        logging.error(f"Failed to send message to Telegram: {e}")


@app.route('/send_message', methods=['POST'])
def handle_message_request():
    data = request.get_json()

    if not data or 'name' not in data or 'email' not in data or 'message' not in data:
        return jsonify({'success': False, 'error': 'Bad Request',
                        'message': 'Request must have name, email and message fields'}), 400

    name = data['name']
    email = data['email']
    message = data['message']

    try:
        send_email(name, email, message)
        send_telegram_message_task.delay(name, email, message)
        return jsonify({'success': True, 'message': 'Email sent successfully'}), 200
    except Exception as e:
        logging.error(f'Failed to send email: {e}')
        return jsonify({'success': False, 'error': 'Internal Server Error',
                        'message': 'An error occurred while sending email, try again later'}), 500


if __name__ == '__main__':
    app.run(debug=True)

