import logging
import os
from datetime import datetime

logs_dir = os.path.join(os.getcwd(), "logs")
os.makedirs(logs_dir, exist_ok=True)

log_filename = datetime.now().strftime("%m_%d_%Y_%H_%M_%S") + ".log"
log_filepath = os.path.join(logs_dir, log_filename)

print("Saving logs to:", log_filepath)

logging.basicConfig(
    filename=log_filepath,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
