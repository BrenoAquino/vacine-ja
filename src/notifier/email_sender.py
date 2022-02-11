from typing import List
from datetime import datetime
from botocore.exceptions import ClientError

from src.models.schedule import Schedule
from .exceptions import NoOneFoundException, FailureToConnectToSNSException, FailureToSendEmailException

import boto3
import logging

class EmailSender:
    def __init__(self, sender: str):
        self.__ses = boto3.client('ses', region_name='sa-east-1')
        self.__charset = 'UTF-8'
        self.__sender = f'Charles <{sender}>'
        
    
    def __format_schedule_message(self, schedule: Schedule) -> str:
        """
        Format the schedule to sentence.
        
        Parameters
        ----------
        schedule : Schedule
            Schedule to be formatted.
            
        Returns
        -------
        str
            Formatted sentence.
        """
        return schedule.name + \
           ' nascido em ' + \
           schedule.birth_date + \
           ' tomará a ' + \
           schedule.dose + \
           ' no dia ' + \
           schedule.target_date + \
           ' as ' + \
           schedule.target_time + \
           ' no ' + \
           schedule.target_place
        
        
    def send_email(self, schedules: List[Schedule], destionations: List[str]):
        """
        Send email to the destionations with the schedules informations.
        
        Parameters
        ----------
        schedules : List[Schedule]
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
        if len(schedules) <= 0:
            raise NoOneFoundException()
        
        schedules_messages = [self.__format_schedule_message(schedule) for schedule in schedules]
        subject = 'Charles - Relatorio do Vacine Já'
        body_text = 'Charles procurou os C.P.F.s e nomes registrados no vacine já.\r\n' + \
                    'Caso queira olhar você mesmo basta acessar https://vacinacao.sms.fortaleza.ce.gov.br/pesquisa/agendados ' + \
                    'e pesquisar pelo seu C.P.F. ou nome.\r\n\n\n' + \
                    '\n\n'.join(schedules_messages) + \
                    '\n\n\nAtualziado em ' + datetime.today().strftime("%d/%m/%Y 'as' %H:%M:%S")
        
        try:
            self.__ses.send_email(
                Destination={
                    'ToAddresses': destionations,
                },
                Message={
                    'Body': {
                        'Text': {
                            'Charset': self.__charset,
                            'Data': body_text,
                        },
                    },
                    'Subject': {
                        'Charset': self.__charset,
                        'Data': subject,
                    },
                },
                Source=self.__sender
            )
            logging.info('Email sent!')
            
        except ClientError as e:
            logging.error(e.response['Error']['Message'])
            raise FailureToConnectToSNSException()
        
        except Exception as e:
            logging.error(e)
            raise FailureToSendEmailException()