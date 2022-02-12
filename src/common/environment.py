from dotenv import load_dotenv
import os

load_dotenv()

PEOPLE = [tuple(single_peoples.split('@')) for single_peoples in os.getenv('PEOPLE').split('|')]

SENDER_EMAIL = os.getenv('SENDER_EMAIL')
DESTINATION_EMAIL = os.getenv('DESTINATION_EMAIL').split('|')

PDF_LIMIT = 10
PREFIX_DATE = 'dia '