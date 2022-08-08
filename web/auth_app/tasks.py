from django.template.loader import get_template

from auth_app.services import send_email
from src.celery import app


@app.task()
def send_verification_email(content, to_email):
    subject = f'Please verify your E-mail Address'
    template = get_template('email/confirmation.html')
    send_email(subject, template, content, to_email)
