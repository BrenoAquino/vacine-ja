import requests

from src.common.environment import SENDER_EMAIL, DESTINATION_EMAIL, PEOPLE
from src.models.people import People
from src.services.vacine_ja import VacineJaService
from src.services.pdf_handler import PdfsService
from src.notifier.email_sender import EmailSender

def handler(event, context):
    session = requests.Session()
    vacine_ja_service = VacineJaService(session)
    
    pdfs_paths = vacine_ja_service.get_pdfs()
    pdfs_service = PdfsService(pdfs_paths)
    
    people = [People(person[0], person[1]) for person in PEOPLE]
    schedules = pdfs_service.search_for_people(people)
    pdfs_service.delete_pdfs()
    
    notifier = EmailSender(SENDER_EMAIL)
    notifier.send_email(schedules, DESTINATION_EMAIL)