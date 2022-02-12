import logging

FILE_NAME = 'logs.log'

def __disable_logger(module: str):
    logger = logging.getLogger(module)
    logger.disabled = True
    logger.propagate = False

def setup_logging():
    __disable_logger('pdfminer')
    __disable_logger('camelot')
    __disable_logger('botocore')
    
    # logging.basicConfig(filename=FILE_NAME, format='%(asctime)s:%(levelname)s:%(name)s:%(message)s', datefmt='%d-%m-%yT%H:%M:%S', level=logging.INFO)
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s', datefmt='%d-%m-%yT%H:%M:%S', level=logging.INFO)