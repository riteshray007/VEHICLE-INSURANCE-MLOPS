import os
import logging
from logging.handlers import RotatingFileHandler
from from_root import from_root
from datetime import datetime

LOG_DIR = 'logs'
LOG_FILE = f"{datetime.now().strftime('%d_%m_%y_%H_%M')}.log"
MAX_LOG_SIZE = 5*1024*1024   #----> 5mb
BACKUP_COUNT = 3 # ---> number of backup files to keep

log_dir_path = os.path.join(from_root() , LOG_DIR)
os.makedirs(log_dir_path , exist_ok=True)
log_file_path = os.path.join( log_dir_path , LOG_FILE )

def configure_logger():
      """
      configure logging with a rotating file handler and a console handler.
      """
      # create a custom logger
      logger = logging.getLogger()
      logger.setLevel(logging.DEBUG)
      
      # define formatter
      formatter = logging.Formatter("[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s ")
      
      # setting up console logger 
      console_handler = logging.StreamHandler()
      console_handler.setLevel(logging.INFO)
      console_handler.setFormatter(formatter)
      
      # a new logger obj with rotating file handler
      file_handler = RotatingFileHandler(log_file_path , maxBytes=MAX_LOG_SIZE , backupCount=BACKUP_COUNT,)
      file_handler.setLevel(logging.DEBUG)
      file_handler.setFormatter(formatter)
      
      logger.addHandler(console_handler)
      logger.addHandler(file_handler)
      
      
# call the method that configures the logger
configure_logger()
      
      
      
            