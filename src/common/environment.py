from dotenv import load_dotenv
import os

load_dotenv()

CPFs = os.getenv('CPFS').split('|')
NAMES = os.getenv('NAMES').split('|')

SENDER_EMAIL = os.getenv('SENDER_EMAIL')
DESTINATION_EMAIL = os.getenv('DESTINATION_EMAIL').split('|')

PDF_LIMIT = 10
PREFIX_DATE = 'dia '