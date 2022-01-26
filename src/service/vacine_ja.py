import json
from turtle import st

from requests import Session
from types import SimpleNamespace
from bs4 import BeautifulSoup

from .exceptions import UnavailableTokenException, InvalidSearchReponseException

def extract_token(session: Session):
    """
    Extract token from the page
    
    Parameters
    ----------
    session : requests.Session
        Session to use
        
    Returns
    -------
    token : str
        Token to validate next request
        
    Raises
    ------
    UnavailableTokenException
        If the token is not available
    """
    response = session.get('https://vacinacao.sms.fortaleza.ce.gov.br/pesquisa/agendados')
    response.raise_for_status()
    
    try:
        bs = BeautifulSoup(response.text, 'html.parser')
        token = bs.find('input', { 'name': '_token' })
        return token['value']
    except:
        raise UnavailableTokenException()

    
def search_for_people(session: Session, token: str, page: int, name: str = '', cpf: str = ''):
    """
    Search for people by name or cpf
    
    Parameters
    ----------
    session : requests.Session
        Session to use
    token : str
        Token to validate the request
    page : int
        Page number
    name : str
        Name to search
    cpf : str
        CPF to search
        
    Raises
    ------
    InvalidSearchReponseException
        If the response is not a json.
    """
    response = session.post(
        'https://vacinacao.sms.fortaleza.ce.gov.br/pesquisa/grid', 
        headers={
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRF-TOKEN': token
        },
        params={
            '_token': token,
            'tipo_pesquisa': 'agendados',
            'nome': name,
            'cpf': cpf,
            'activePage': page
        }
    )
    response.raise_for_status()
    
    try:
        json_response = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
        return json_response
    
    except:
        raise InvalidSearchReponseException()