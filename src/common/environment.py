from dotenv import load_dotenv
import os

load_dotenv()

CPFs = os.getenv('CPFs').split('|')
NAMES = os.getenv('NAMES').split('|')

AWS_ACCESS_KEY = os.getenv('ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.getenv('SECRET_ACCESS_KEY')
AWS_REGION_NAME = os.getenv('REGION_NAME')