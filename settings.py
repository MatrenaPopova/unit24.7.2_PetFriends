import os

from dotenv import load_dotenv

load_dotenv()

valid_email = os.getenv('valid_email')
valid_password = os.getenv('valid_password')

incorrect_email = os.getenv('incorrect_email')
incorrect_password = os.getenv('incorrect_password')