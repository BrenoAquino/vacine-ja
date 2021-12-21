from src.common.environment import CPFs, NAMES
from src.service import extract_token, search_for_people
from src.communication import send_email

from src.service.exceptions import UnavailableTokenException
from src.communication.exceptions import NoOneFoundException

import requests
import logging

def is_finished(content):
    return len(content.rows) < content.rowsPerPage


def main(event, context):
    peoples = []
    
    for cpf in CPFs:
        if len(cpf) != 14:
            continue
        
        logging.info(f'Searching for CPF: {cpf}')
        page = 1
        while True:
            try:
                session = requests.Session()
                token = extract_token(session)
                response = search_for_people(session, token, page, cpf=cpf)
                peoples.extend(response.rows)
                page += 1
                if is_finished(response):
                    break
            except UnavailableTokenException:
                logging.error('Could not get token while searching for CPF: {cpf}')
                break
            except:
                logging.error(f'Something went wrong while searching for CPF: {cpf}')
                break
            
    for name in NAMES:
        if len(name) <= 0:
            continue
        
        logging.info(f'Searching for name: {name}')
        page = 1 
        while True:
            try:
                session = requests.Session()
                token = extract_token(session)
                response = search_for_people(session, token, page, name=name)
                peoples.extend(response.rows)
                page += 1
                if is_finished(response):
                    break
            except UnavailableTokenException:
                logging.error('Could not get token while searching for name: {name}')
                break
            except:
                logging.error(f'Something went wrong while searching for name: {name}')
                break
    
    try:
        send_email(peoples)
    except NoOneFoundException:
        logging.error('No one found in vacine ja list')
    except Exception as e:
        logging.error('Something went wrong while sending email')