import sys
from src.logger import logging

def error_details(exc: BaseException) -> str:
    _, _, exc_tb = sys.exc_info() 
    if exc_tb is None:
        return f"{type(exc).__name__}: {exc}"
    while exc_tb.tb_next:
        exc_tb = exc_tb.tb_next
    file_name = exc_tb.tb_frame.f_code.co_filename
    return f"{type(exc).__name__}: {exc} at {file_name}:{exc_tb.tb_lineno}"

class CustomException(Exception):
    def __init__(self, exc: BaseException):
        super().__init__(str(exc))
        self.details = error_details(exc)
        
    def __str__(self):
        return self.details

if __name__ == "__main__":
    try: 
        a = 1/0
    except Exception as e: 
        logging.info("Division by zero") 
        raise CustomException(e)