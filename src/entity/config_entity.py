
import os
from src.constants import *
from dataclasses import dataclass
from datetime import datetime

TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")

@dataclass
class TrainingPipelineConfig:
    pipeline_name: str = PIPELINE_NAME
    artifact_dir: str = os.path.join(ARTIFACT_DIR, TIMESTAMP)
    timestamp: str = TIMESTAMP

training_pipeline_config: TrainingPipelineConfig = TrainingPipelineConfig()


@dataclass
class DataIngestionConfig:
    """
    inside entity/confi_entity - class DataIngestionConfig
    prepares pre-requisite file,folder path and variables
    """    
    data_ingestion_dir: str = os.path.join(training_pipeline_config.artifact_dir, DATA_INGESTION_DIR_NAME)
    feature_store_file_path: str = os.path.join(data_ingestion_dir, DATA_INGESTION_FEATURE_STORE_DIR, FILE_NAME)
    training_file_path: str = os.path.join(data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TRAIN_FILE_NAME)
    testing_file_path: str = os.path.join(data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TEST_FILE_NAME)
    train_test_split_ratio: float = DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
    collection_name:str = DATA_INGESTION_COLLECTION_NAME
    database:str = DATABASE_NAME
    

@dataclass
class DataValidationConfig:
    """
    inside entity/config_entity - DataValidationConfig
    prepares pre-requisite dir paths for datavalidation
    """
    
    data_validation_dir:str = os.path.join(training_pipeline_config.artifact_dir,DATA_VALIDATION_DIR_NAME)
    validation_report_file_path:str = os.path.join(data_validation_dir , DATA_VALIDATION_REPORT_FILE_NAME)
    
    