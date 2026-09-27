import os
import sys
import json

from src.entity.config_entity import DataValidationConfig
from src.entity.artifact_entity import DataIngestionArtifact , DataValidationArtifact
from src.utils.main_utils import read_yaml_file , load_DataFrame , write_yaml_file
from src.logger import logging
from src.exception import MyException
from src.constants import SCHEMA_FILE_PATH
import pandas as pd
from pandas import DataFrame
class DataValidation:
      
      def __init__(self, data_ingestion_artifact:DataIngestionArtifact , data_validation_config:DataValidationConfig ):
            """
            :param data_ingestion_artifact: Output reference of data ingestion artifact stage
            :param data_validation_config: configuration for data validation
            """            
            try:
                  self.data_ingestion_artifact = data_ingestion_artifact
                  self.data_validation_config = data_validation_config
                  self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
            except Exception as e:
                  raise MyException(e,sys) from e
            
      
            
      def validate_number_of_columns(self,dataframe:DataFrame)->bool:
            """
            Method Name :   validate_number_of_columns
            Description :   This method validates the number of columns
            
            Output      :   Returns bool value based on validation results
            On Failure  :   Write an exception log and then raise an exception
            """
            try:
                  status = len(self._schema_config["columns"]) == len(dataframe.columns)
                  logging.info(f' is required column length satisfied - {status}')
                  return status
            except Exception as e:
                  raise MyException(e , sys ) from e
      
      
      def is_column_exist(self , df:DataFrame )->bool:
            """
            Method Name :   is_column_exist
            Description :   This method validates the existence of a numerical and categorical columns
            
            Output      :   Returns bool value based on validation results
            On Failure  :   Write an exception log and then raise an exception
            """
            
            try:
                  df_cols = df.columns
                  missing_num_col = []
                  missing_cat_col = []
                  
                  for col in self._schema_config['numerical_columns']:
                        if col not in df_cols:
                              missing_num_col.append(col)
                  if len(missing_num_col) > 0:
                        logging.warning(f'missing numerical cols - {missing_num_col}')
                  
                  for col in self._schema_config['categorical_columns']:
                        if col not in df_cols:
                              missing_cat_col.append(col)
                  if len(missing_cat_col) > 0:
                        logging.warning(f'missing categorical cols - {missing_cat_col}')                  
                  
                  return (len(missing_num_col) == 0) and (len(missing_cat_col) == 0)
                  
            except Exception as e:
                  raise MyException(e,sys) from e
                  
      def initiate_data_validation(self) -> DataValidationArtifact:
          """
          Description :   This method initiates the data validation component for the pipeline
          
          Output      :   Returns bool value based on validation results
          On Failure  :   Write an exception log and then raise an exception
          """      
          try:
              validation_error_msg = ""
              logging.info("Starting data validation process...")
              
              train_df = load_DataFrame(file_path=self.data_ingestion_artifact.trained_file_path)
              test_df = load_DataFrame(file_path=self.data_ingestion_artifact.test_file_path)
              
              # 1. Validate total column count
              if not self.validate_number_of_columns(dataframe=train_df):
                  validation_error_msg += "Column count mismatch in training dataframe. "
              else:
                  logging.info("Train dataframe column count validated successfully.")
      
              if not self.validate_number_of_columns(dataframe=test_df):
                  validation_error_msg += "Column count mismatch in testing dataframe. "
              else:
                  logging.info("Test dataframe column count validated successfully.")
                  
              # 2. Validate column schema and types
              if not self.is_column_exist(df=train_df):
                  validation_error_msg += "Required numerical/categorical columns missing in training dataframe. "
              else:
                  logging.info("Train dataframe schema validated successfully.")
      
              if not self.is_column_exist(df=test_df):
                  validation_error_msg += "Required numerical/categorical columns missing in testing dataframe. "
              else:
                  logging.info("Test dataframe schema validated successfully.")
                  
              validation_status = len(validation_error_msg) == 0
                             
              # Create output directory
              report_dir = os.path.dirname(self.data_validation_config.validation_report_file_path)
              os.makedirs(report_dir, exist_ok=True)
      
              # Save validation report
              validation_report = {
                  "validation_status": validation_status,
                  "message": validation_error_msg.strip()
              }
              
              write_yaml_file(
                  file_path=self.data_validation_config.validation_report_file_path, 
                  content=validation_report
              )

              if not validation_status:
                  logging.error(f"Data Validation failed with following issues : {validation_error_msg.strip()}")
                  raise Exception(f"Data Validation failed: {validation_error_msg.strip()}")
            
              data_validation_artifact = DataValidationArtifact(
                  validation_status=validation_status,
                  message=validation_error_msg.strip(),
                  validation_report_file_path=self.data_validation_config.validation_report_file_path
              )
              
              logging.info(f"Data validation artifact created: {data_validation_artifact}")
              return data_validation_artifact
      
          except Exception as e:
              raise MyException(e, sys) from e
                  
            

