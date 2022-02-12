import logging
import requests

from src.common.environment import SENDER_EMAIL, DESTINATION_EMAIL, PEOPLE
from src.models.people import People
from src.services.vacine_ja import VacineJaService
from src.services.pdf_handler import PdfsService
from src.notifier.email_sender import EmailSender

from src.services.exceptions import FailureToConnectVacineJaException, InvalidPdfsResponseException, InvalidPdfsResponseFormatException
from src.notifier.exceptions import FailureToConnectToSNSException, FailureToSendEmailException, NoOneFoundException

def handler(event, context):
    try:
        logging.info('Getting PDFs from Vacine Ja')
        session = requests.Session()
        vacine_ja_service = VacineJaService(session)
        pdfs_paths = vacine_ja_service.get_pdfs()
        
        logging.info('Searching for people')
        pdfs_service = PdfsService(pdfs_paths)
        people = [People(person[0], person[1]) for person in PEOPLE]
        schedules = pdfs_service.search_for_people(people)
        
        logging.info('Sending emails')
        notifier = EmailSender(SENDER_EMAIL)
        notifier.send_email(schedules, DESTINATION_EMAIL)
        logging.info('Success:Email sent')
        
    except NoOneFoundException:
        logging.info('Success:No one found')
        
    except FailureToConnectVacineJaException:
        logging.error('Error:FailureToConnectVacineJaException')
    
    except InvalidPdfsResponseException:
        logging.error('Error:InvalidPdfsResponseException')
    
    except InvalidPdfsResponseFormatException:
        logging.error('Error:InvalidPdfsResponseFormatException')
    
    except FailureToConnectToSNSException:
        logging.error('Error:FailureToConnectToSNSException')
    
    except FailureToSendEmailException:
        logging.error('Error:FailureToSendEmailException')