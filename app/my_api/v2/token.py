from itsdangerous import URLSafeTimedSerializer
import os
import app


def generate_token(email):
    return URLSafeTimedSerializer(os.getenv('SECRET_KEY')).dumps(email)


def confirm_token(email_token, salt=os.getenv('USER_SALT'), expiration=3600):
    return URLSafeTimedSerializer(os.getenv('SECRET_KEY')).loads(email_token, salt, expiration)
