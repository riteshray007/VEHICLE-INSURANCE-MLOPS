import os
from datetime import date

# for mongodb connection
DATABASE_NAME  = 'Proj1'
# COLLECTION_NAME = 'Proj1-Data'
MONGODB_URL_KEY = 'MONGODB_URL'

PIPELINE_NAME: str = ""
ARTIFACT_DIR: str = "artifact"

MODEL_FILE_NAME = "model.pkl"

TARGET_COLUMN = "Response"
CURRENT_YEAR = date.today().year
PREPROCSSING_OBJECT_FILE_NAME = "preprocessing.pkl"

FILE_NAME: str = "data.csv"
TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"
SCHEMA_FILE_PATH = os.path.join("config", "schema.yaml")

# DATA INGESTION RELATED CONSTANTS
DATA_INGESTION_COLLECTION_NAME:str='Proj1-Data'
DATA_INGESTION_DIR_NAME:str='data_ingestion'
DATA_INGESTION_FEATURE_STORE_DIR:str='feature_store'
DATA_INGESTION_INGESTED_DIR:str='ingested'
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float= 0.25


# data validation related constants 
DATA_VALIDATION_DIR_NAME:str='data_validation'
DATA_VALIDATION_REPORT_FILE_NAME:str='report.yaml'


"""
Data Transformation ralated constant start with DATA_TRANSFORMATION VAR NAME
"""
DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"
PREPROCSSING_OBJECT_FILE_NAME = "preprocessing.pkl"
TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"


# model training realated constants 

MODEL_TRAINER_DIRNAME:str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR:str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME:str = "model.pkl"
MODEL_TRAINER_TRAINED_MODEL_METRICS:str = 'metrics.yaml'
MODEL_TRAINER_EXPECTED_SCORE:float = 0.7
BEST_PARAMS_PATH = os.path.join("config", "model.yaml")


# aws credentials
AWS_ACCESS_KEY_ID_ENV_KEY = "AWS_ACCESS_KEY_ID"
AWS_SECRET_ACCESS_KEY_ENV_KEY = "AWS_SECRET_ACCESS_KEY"
REGION_NAME = "us-east-1"

"""
MODEL Evaluation related constants
"""
MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE: float = 0.02
MODEL_BUCKET_NAME = "vehicle-insurance-proj-s3"
MODEL_PUSHER_S3_KEY = "model-registry"