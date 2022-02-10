from src.functions.checker.main import handler as checker_handler
from src.functions.reader.main import handler as reader_handler
import logging

logging.basicConfig(level=logging.INFO)

# checker_handler(None, None)
reader_handler(None, None)