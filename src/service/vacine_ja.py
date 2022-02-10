import json

from typing import List
from requests import Session
from datetime import datetime
from src.common.environment import PREFIX_DATE

from .exceptions import InvalidPdfsResponseException, InvalidPdfsResponseFormatException
    
def extract_pdfs_infos(session: Session):
    """
    Extract pdf links from the page
    
    Parameters
    ----------
    session : requests.Session
        Session to use
        
    Returns
    -------
    pdf_links : List[str]
        List of pdf links
        
    Raises
    ------
    InvalidPdfsResponseException
        If the response is not a json.
    """
    response = session.get('https://docs.google.com/spreadsheets/d/1IJBDu8dRGLkBgX72sRWKY6R9GfefsaDCXBd3Dz9PZNs/gviz/tq?gid=970021343')
    response.raise_for_status()
    
    try:
        start_json_index = response.text.find('{')
        end_json_index = response.text.rfind('}')
        
        response_formatted = response.text[start_json_index:end_json_index + 1]
        json_response = json.loads(response_formatted)
        return json_response
    except:
        raise InvalidPdfsResponseException()
    
    
def format_table_to_pdf_object(response: dict, limit: int) -> List[dict]:
    """
    Format table to pdf object
    
    Parameters
    ----------
    table : list
        List of table
    limit : int
        Limit of pdfs to return
        
    Returns
    -------
    pdf_object : dict
        Pdf object
    """
    pdfs = []
    table: dict = response.get('table')
    rows: List[dict] = table.get('rows')
    if rows is None or len(rows) == 0:
        raise InvalidPdfsResponseFormatException()
    
    # Getting Filds Names
    keys = rows[0].get('c')
    if keys is None:
        raise InvalidPdfsResponseFormatException()
    keys = list(map(lambda key: key.get('v'), keys))
    
    # Getting Filds Values
    pdfs_infos = rows[1:limit + 1]
    for pdf_info in pdfs_infos:
        values = pdf_info.get('c')
        if values is None or len(values) != len(keys):
            raise InvalidPdfsResponseFormatException()
        values = list(map(lambda value: value.get('v'), values))
        
        # Creating pdf object
        pdf = {}
        for key, value in zip(keys, values):
            pdf[key] = value
        
        def extract_date_from_title(title: str, prefix_date: str) -> datetime or None:
            date = None
            date_start_index = title.rfind(prefix_date)
            if date_start_index >= 0:
                date_string = title[date_start_index:]
                date = datetime.strptime(date_string, f"{prefix_date}%d/%m/%Y")
            return date
        pdf['date'] = extract_date_from_title(pdf['titulo'], PREFIX_DATE)
        pdfs.append(pdf)
        
    return pdfs


def get_lastest_pdfs(pdfs: List[dict]) -> List[dict]:
    """
    Filter pdfs by date to return only the lastest pdfs.
    
    Parameters
    ----------
    pdfs : list
        List of pdfs
        
    Returns
    -------
    pdfs : list
        List of pdfs
    """
    lastest_pdf = max(pdfs, key=lambda pdf: pdf.get('date'))
    all_pdfs_with_lastest_date = list(filter(lambda pdf: pdf.get('date') == lastest_pdf.get('date'), pdfs))
    return all_pdfs_with_lastest_date


def download_pdfs(session: Session, pdfs: List[dict]) -> List[str]:
    """
    Download pdfs
    
    Parameters
    ----------
    pdfs : List[dict]
        List of pdfs
        
    Returns
    -------
    List[str]
        List of pdfs paths
    """
    paths = []
    for pdf in pdfs:
        title: str = pdf.get('titulo')
        url: str = pdf.get('pdf')
        
        try:
            response = session.get(url)
            response.raise_for_status()
        except:
            continue
        
        pdf_title = title.replace('/', '-')
        with open(f'tmp/{pdf_title}.pdf', 'wb') as file:
            file.write(response.content)
            paths.append(f'tmp/{pdf_title}.pdf')
    return paths