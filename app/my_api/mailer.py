import os
import app
from flask_mail import Mail
from flask import render_template
from flask_mail import Message


def send_email(to, subject, template):
    msg = Message(
        subject, recipients=[to], html=template,
        sender=os.getenv('DEFAULT_SENDER'))
    Mail().send(msg)
