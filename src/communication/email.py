from typing import List
from datetime import datetime
from botocore.exceptions import ClientError

from src.common.environment import SENDER_EMAIL, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION_NAME
from src.common.people_info_formatter import people_info_formatter
from .exceptions import NoOneFoundException, FailureToConnectToSNSException, FailureToSendEmailException

import boto3
import logging

def send_email(people: List[str], destionations: List[str]):
    """
    Send email to the destionations with the people informations.
    
    Parameters
    ----------
    people : List[str]
        List of people with their informations.
    destionations : List[str]
        List of emails to send the email to.
        
    Raises
    ------
    NoOneFoundException
        If there is no one to send the email.
    FailureToConnectToSNSException
        If there is a problem to connect to SNS.
    FailureToSendEmailException
        If there is any problem. 
    """
    if len(people) <= 0:
        raise NoOneFoundException()
    
    people_formatted = [people_info_formatter(p) for p in people]
    charset = 'UTF-8'
    sender = f'Charles <{SENDER_EMAIL}>'
    subject = 'Charles - Relatorio do Vacine Já'
    body_text = 'Charles procurou os C.P.F.s e nomes registrados no vacine já.\r\n' + \
                'Caso queira olhar você mesmo basta acessar https://vacinacao.sms.fortaleza.ce.gov.br/pesquisa/agendados ' + \
                'e pesquisar pelo seu C.P.F. ou nome.\r\n\n\n' + \
                '\n\n'.join(people_formatted) + \
                '\n\n\nAtualziado em ' + datetime.today().strftime("%d/%m/%Y 'as' %H:%M:%S")

    try:
        client = boto3.client('ses',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION_NAME
        )
        
        client.send_email(
            Destination={
                'ToAddresses': destionations,
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': charset,
                        'Data': body_text,
                    },
                },
                'Subject': {
                    'Charset': charset,
                    'Data': subject,
                },
            },
            Source=sender
        )
        logging.info('Email sent!')
        
    except ClientError as e:
        logging.error(e.response['Error']['Message'])
        raise FailureToConnectToSNSException()
    
    except Exception as e:
        logging.error(e)
        raise FailureToSendEmailException()