import os
import sys
import pandas as pd
from pandas import DataFrame
import numpy as np
from src.entity.artifact_entity import DataIngestionArtifact , DataValidationArtifact, DataTransformationArtifact
from src.logger import logging
from src.exception import MyException
from src.entity.config_entity import DataTransformationConfig
from src.constants import SCHEMA_FILE_PATH , TARGET_COLUMN
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler,StandardScaler , OneHotEncoder , OrdinalEncoder
from sklearn.pipeline import Pipeline
from imblearn.combine import SMOTEENN
from src.utils.main_utils import save_obj , save_numpy_array_data , read_yaml_file , load_DataFrame

class DataTransformation:
      """
      constructor
      :param data_ingestion_artifact: artifact variables produced by ingestion pipeline
      :param data_transformation_config: configuration variables of data transformation
      """
      def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                   data_transformation_config:DataTransformationConfig):
          try:
                self.data_ingestion_artifact=data_ingestion_artifact
                self.data_transformation_config=data_transformation_config
                self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
          except Exception as e :
                raise MyException(e,sys)
          
      def get_data_transformer_object(self)-> Pipeline:
            """
            Creates and returns a data transformer object for the data, 
            including MinMax scaling , Standard scaling , OneHotEncoding
            Ordinal encoding using column transformer inside a sklearn PipeLine
            """            
            mm_column = self._schema_config['mm_columns']
            num_column = self._schema_config['num_features']
            ohe_column = self._schema_config['ohe_columns']
            ordinal = self._schema_config['ordinal_columns']
            
            # Define ordinal ordering for Vehicle_Age
            vehicle_age_cat = [['< 1 Year', '1-2 Years', '> 2 Years']]
    
            # Build ColumnTransformer
            preprocessor = ColumnTransformer(
                  transformers=[
                        ("standarScaler" , StandardScaler() ,  num_column ),
                        ("minMaxScaler" , MinMaxScaler() , mm_column ),
                        ("oneHotEncoder" , 
                         OneHotEncoder(drop='first' , sparse_output=False , dtype=int , handle_unknown='ignore') , 
                         ohe_column ),
                        ("ordinalEncoder" , 
                         OrdinalEncoder(categories=vehicle_age_cat , handle_unknown='use_encoded_value' , unknown_value=-1),
                         ordinal)
                  ],
                  remainder="passthrough",
                  verbose_feature_names_out=False
            )
            # Set transformer output to Pandas DataFrame (Scikit-Learn 1.2+)
            preprocessor.set_output(transform='pandas')
            
            # Final unified pipeline
            final_pipeline = Pipeline(steps=[
                  ("preprocessor" , preprocessor )
            ])
            
            logging.info("tranformation pipeline created and returned ")
            logging.info("existing get_data_transformation_object function ")
            return final_pipeline
            
      def _drop_id_column(self,df:DataFrame)->DataFrame:
            """
            drops id of the given df, if it exists
            located at data_transformation.py in src/components 
            """
            drop_col = self._schema_config['drop_columns']
            if drop_col in df.columns:
                  df.drop(columns=[drop_col],inplace=True)
            return df
      
      
      
      def initiate_data_transformation(self)->DataTransformationArtifact:
            """
            Initiates the data transformation component for the pipeline.
            """            
            logging.info("entered into initiate_data_transformation method of DataTransformation class ")
            try:
                  train_df = load_DataFrame(self.data_ingestion_artifact.trained_file_path)
                  test_df = load_DataFrame(self.data_ingestion_artifact.test_file_path)
                  
                  logging.info("train and test df loaded")
                  
                  input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN])
                  target_feature_train_df = train_df[TARGET_COLUMN]
                  
                  input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN])
                  target_feature_test_df = test_df[TARGET_COLUMN]
                  
                  logging.info("input and target cols defined for both train & test df ")
                  
                  input_feature_train_df = self._drop_id_column(input_feature_train_df)
                  input_feature_test_df = self._drop_id_column(input_feature_test_df)
                  
                  logging.info("starting data custom pipeline after removing id cols ")
                  logging.info("getting preprocessor pipeline object ")
                  preprocessor = self.get_data_transformer_object()
                  logging.info("got preprocessor pipeline object ")
                  
                  logging.info("initializing pre processor pipeline object for train df")
                  input_feature_train_array = preprocessor.fit_transform(input_feature_train_df)
                  logging.info("initializing pre processor pipeline object for test df")
                  input_feature_test_array = preprocessor.transform(input_feature_test_df)
                  logging.info("transformed train & test df's ")
                  
                  logging.info("applying smottee technique to only the train df")
                  smt = SMOTEENN(sampling_strategy='minority')
                  input_feature_train_final , target_feature_train_df = smt.fit_resample(input_feature_train_array , target_feature_train_df)
                  logging.info("smottee applied to train df ")
                  
                  train_arr = np.c_[input_feature_train_final , np.array(target_feature_train_df) ]
                  test_arr = np.c_[input_feature_test_array , np.array(target_feature_test_df) ]
                  logging.info("feature-target concatenation done for train-test df.")
                  
                  save_obj(self.data_transformation_config.transformed_object_file_path , preprocessor)
                  save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,train_arr)
                  save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,test_arr)
                  
                  logging.info("object saved , train & test arr saved ")
                  logging.info("Data Transformation completed sucessfully")
                  
                  return DataTransformationArtifact(
                        self.data_transformation_config.transformed_object_file_path,
                        self.data_transformation_config.transformed_train_file_path,
                        self.data_transformation_config.transformed_test_file_path
                  )
      
            except Exception as e:
                  raise MyException(e , sys ) from e

