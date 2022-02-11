import requests

from src.common.environment import SENDER_EMAIL, DESTINATION_EMAIL
from src.models.people import People
from src.services.vacine_ja import VacineJaService
from src.services.pdf_handler import PdfsService
from src.notifier.email_sender import EmailSender

def handler(event, context):
    session = requests.Session()
    vacine_ja_service = VacineJaService(session)
    
    pdfs_paths = vacine_ja_service.get_pdfs()
    pdfs_service = PdfsService(pdfs_paths)
    
    people = [People('ADAIL SILVA DE ARAUJO', '18/10/1982')]
    schedules = pdfs_service.search_for_people(people)
    
    notifier = EmailSender(SENDER_EMAIL)
    notifier.send_email(schedules, DESTINATION_EMAIL)