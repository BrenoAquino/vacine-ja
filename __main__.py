from src.common.setup_logging import setup_logging
from src.functions.pdf_reader.main import handler as pdf_reader_handler
from src.functions.health_check.main import handler as health_check_handler

setup_logging()
pdf_reader_handler(None, None)
# health_check_handler(None, None)