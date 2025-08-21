import os
from src.exception import CustomException
from src.logger import logging
import joblib

def save_object(obj, filename):
    try: 
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        joblib.dump(obj, filename)
        logging.info(f'Object succsessfully saved to: {filename}')
        return True
        
    except Exception as e: 
        logging.exception('Joblib object saving failed!')
        raise CustomException(f'Error saving object to {filename} as {e}')
    