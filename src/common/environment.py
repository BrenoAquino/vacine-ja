from dotenv import load_dotenv
import os

load_dotenv()

CPFs = os.getenv('CPFS').split('|')
NAMES = os.getenv('NAMES').split('|')

SENDER_EMAIL = os.getenv('SENDER_EMAIL')
DESTINATION_EMAIL = os.getenv('DESTINATION_EMAIL').split('|')

AWS_ACCESS_KEY_ID = os.getenv('AUTH_AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AUTH_AWS_SECRET_ACCESS_KEY')
AWS_REGION_NAME = os.getenv('AUTH_AWS_REGION_NAME')