# checking local packaging and logger

# from src.logger import logging

# logging.debug("debug msg ")
# logging.info("This is an info message.")
# logging.warning("This is a warning message.")
# logging.error("This is an error message.")
# logging.critical("This is a critical message.")

# --------------------------------------------
# checking custom Exception 

# from src.exception import MyException
# import sys

# try:
#       print(1+'z')
# except Exception as e:
#       logging.error(e)
#       raise MyException(e, sys) from e

# --------------------------------------------------

from src.pipeline.training_pipeline import TrainPipeline

pipline = TrainPipeline()
# print(pipline.data_ingestion_config)
pipline.run_pipeline()