import requests

from src.common.environment import PDF_LIMIT
from src.service.vacine_ja import extract_pdfs_infos, format_table_to_pdf_object, get_lastest_pdfs, download_pdfs

def handler(event, context):
    session = requests.Session()
    
    response = extract_pdfs_infos(session)
    pdfs = format_table_to_pdf_object(response, PDF_LIMIT)
    lastest_pdfs = get_lastest_pdfs(pdfs)
    pdfs_paths = download_pdfs(session, lastest_pdfs)
    
    for path in pdfs_paths:
        tables = camelot.read_pdf(path, pages = '1', multiple_tables = True)
        text = extract_text(path)
        # reader = PyPDF2.PdfFileReader(path)
        # text = ''
        # for page in range(reader.getNumPages()):
        #     page_obj = reader.getPage(page)
        #     text += page_obj.extractText()
        #     print(page)
            
        with open('test.txt', 'w') as file:
            file.write(text)
        print(text)
        
    