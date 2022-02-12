import json

from typing import List
from requests import Session
from datetime import datetime

from src.common.environment import PDF_LIMIT
from src.common.environment import PREFIX_DATE
from src.models.pdf import PDF

from .exceptions import InvalidPdfsResponseException, InvalidPdfsResponseFormatException, FailureToConnectVacineJaException
    
class VacineJaService:
    def __init__(self, session: Session):
        self.__session = session


    def __pdfs_from_vacine_ja(self):
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
        FailureToConnectVacineJaException
            If the page could not be reached.
        InvalidPdfsResponseException
            If the response is not a json.
        """
        try:
            response = self.__session.get('https://docs.google.com/spreadsheets/d/1IJBDu8dRGLkBgX72sRWKY6R9GfefsaDCXBd3Dz9PZNs/gviz/tq?gid=970021343')
            response.raise_for_status()
        except:
            raise FailureToConnectVacineJaException()
        
        try:
            start_json_index = response.text.find('{')
            end_json_index = response.text.rfind('}')
            
            response_formatted = response.text[start_json_index:end_json_index + 1]
            json_response = json.loads(response_formatted)
            return json_response
        except:
            raise InvalidPdfsResponseException()
    
    
    def __create_pdf(self, keys: List[str], raw_pdf: dict) -> PDF:
        """
        Create a pdf object from a raw pdf info.
        
        Parameters
        ----------
        keys : List[str]
            List of keys (fields).
        raw_pdf : dict
            Raw pdf info.
            
        Returns
        -------
        PDF
            Pdf object.
            
        Raises
        ------
        InvalidPdfsResponseFormatException
            If the response has not the expected format.
        """
        values = raw_pdf.get('c')
        if values is None or len(values) != len(keys):
            raise InvalidPdfsResponseFormatException()
        values = list(map(lambda value: value.get('v'), values))
        
        def extract_date_from_title(title: str, prefix_date: str) -> datetime or None:
            date = None
            date_start_index = title.rfind(prefix_date)
            if date_start_index >= 0:
                date_string = title[date_start_index:]
                date = datetime.strptime(date_string, f"{prefix_date}%d/%m/%Y")
            return date
        
        pdf_dict = {}
        for key, value in zip(keys, values):
            pdf_dict[key] = value
        pdf_dict['date'] = extract_date_from_title(pdf_dict['titulo'], PREFIX_DATE)
        return PDF(pdf_dict['titulo'], pdf_dict['date'], pdf_dict['pdf'])
    
    
    def __convert_response_to_pdfs(self, response: dict, limit: int) -> List[PDF]:
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
            
        Raises
        ------
        InvalidPdfsResponseFormatException
            If the response has not the expected format.
        """
        pdfs = []
        table: dict = response.get('table')
        rows: List[dict] = table.get('rows')
        if rows is None or len(rows) == 0:
            raise InvalidPdfsResponseFormatException()
        
        # Getting Fields Names
        keys = rows[0].get('c')
        if keys is None:
            raise InvalidPdfsResponseFormatException()
        keys = list(map(lambda key: key.get('v'), keys))
        
        # Getting Fields Values
        pdfs_infos = rows[1:limit + 1]
        for pdf_info in pdfs_infos:
            pdf = self.__create_pdf(keys, pdf_info)
            pdfs.append(pdf)
            
        return pdfs
    
    
    def __filter_lastest_pdfs(self, pdfs: List[PDF]) -> List[PDF]:
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
        lastest_pdf = max(pdfs, key=lambda pdf: pdf.date)
        all_pdfs_with_lastest_date = list(filter(lambda pdf: pdf.date == lastest_pdf.date, pdfs))
        return all_pdfs_with_lastest_date
    
    
    def __download_pdfs(self, pdfs: List[PDF]) -> List[PDF]:
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
        for pdf in pdfs:
            title: str = pdf.title
            url: str = pdf.path
            
            try:
                response = self.__session.get(url)
                response.raise_for_status()
            except:
                continue
            
            pdf_title = title.replace('/', '-')
            with open(f'tmp/{pdf_title}.pdf', 'wb') as file:
                file.write(response.content)
                pdf.path = f'tmp/{pdf_title}.pdf'
        return pdfs
    
    
    def get_pdfs(self) -> List[PDF]:
        """
        Get lastest pdfs and download them.
        
        Returns
        -------
        List[str]
            List of pdfs
            
        Raises
        ------
        FailureToConnectVacineJaException
            If the page could not be reached.
        InvalidPdfsResponseException
            If the response is not a json.
        InvalidPdfsResponseFormatException
            If the response has not the expected format.
        """
        pdfs = self.__pdfs_from_vacine_ja()
        pdfs = self.__convert_response_to_pdfs(pdfs, PDF_LIMIT)
        pdfs = self.__filter_lastest_pdfs(pdfs)
        return self.__download_pdfs(pdfs)