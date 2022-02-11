import numpy
import pandas
import requests
import camelot

from src.common.environment import PDF_LIMIT
from src.service.vacine_ja import extract_pdfs_infos, format_table_to_pdf_object, get_lastest_pdfs, download_pdfs

def handler(event, context):
    session = requests.Session()
    
    response = extract_pdfs_infos(session)
    pdfs = format_table_to_pdf_object(response, PDF_LIMIT)
    lastest_pdfs = get_lastest_pdfs(pdfs)
    pdfs_paths = download_pdfs(session, lastest_pdfs)
    
    for path in pdfs_paths:
        table = camelot.read_pdf(path, pages='1-3', flavor='stream', )
        all_tables_data_frame = [table[n].df for n in range(table.n)]
        data_frame = pandas.concat(all_tables_data_frame)
        
        data_frame[0].replace('', numpy.nan, inplace=True)
        data_frame.dropna(subset=[0], inplace=True)
        
        new_header = data_frame.iloc[0] #grab the first row for the header
        data_frame = data_frame[1:] #take the data less the header row
        data_frame.columns = new_header
        
        data_frame.to_csv(path.replace('.pdf', '.csv'), index=False)
        print(data_frame.head())
        