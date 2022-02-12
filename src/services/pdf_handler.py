import os

from typing import List
from pandas import concat, DataFrame
from camelot import read_pdf
from numpy import nan

from src.models.pdf import PDF
from src.models.people import People
from src.models.schedule import Schedule
    
class PdfsService:
    def __init__(self, pdfs: List[PDF]):
        self.__pdfs = pdfs
    
    
    def __filter_lastest_pdfs(self) -> List[PDF]:
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
        lastest_pdf = max(self.__pdfs, key=lambda pdf: pdf.date)
        all_pdfs_with_lastest_date = list(filter(lambda pdf: pdf.date == lastest_pdf.date, self.__pdfs))
        return all_pdfs_with_lastest_date
    
    
    def __read_pdf(self, pdf: PDF) -> DataFrame:
        pdf_tables = read_pdf(pdf.path, pages='1-3', flavor='stream')
        all_tables_data_frame = [pdf_tables[n].df for n in range(pdf_tables.n)]
        
        data_frame = concat(all_tables_data_frame)
        
        data_frame[0].replace('', nan, inplace=True)
        data_frame.dropna(subset=[0], inplace=True)
        
        new_header = data_frame.iloc[0]
        data_frame = data_frame[1:]
        data_frame.columns = new_header
        
        return data_frame
    
    
    def search_for_people(self, people: List[People]) -> List[Schedule]:
        """
        Search for people in pdfs.
        
        Parameters
        ----------
        people : list
            List of people
            
        Returns
        -------
        schedules : list
            List of schedules
        """
        pdfs = self.__filter_lastest_pdfs()
        schedules = []
        
        for pdf in pdfs:
            pdf_data_frame = self.__read_pdf(pdf)
            
            for single_people in people:
                pdf_data_frame.to_csv('tmp/debug.csv')
                pdf_data_frame
                possibilities = pdf_data_frame[
                    (pdf_data_frame['nome'].str.lower() == single_people.name.lower()) &
                    (pdf_data_frame['data_nascimento'].str.lower() == single_people.birth_date.lower())
                ]
                
                for _, possibility in possibilities.iterrows():
                    schedule = Schedule(
                        name=possibility['nome'],
                        birth_date=possibility['data_nascimento'],
                        dose=possibility['dose'],
                        target_date=possibility['data'],
                        target_time=possibility['hora'],
                        target_place=possibility['localvacinacao'],
                    )
                    schedules.append(schedule)
                    
        return schedules
    
    
    def delete_pdfs(self):
        """
        Delete pdfs
        """
        for pdf in self.__pdfs:
            os.remove(pdf.path)