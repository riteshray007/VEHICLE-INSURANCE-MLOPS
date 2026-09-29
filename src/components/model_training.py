import os
import sys
import pandas as pd
import numpy as np
from pandas import DataFrame
from dataclasses import asdict

from src.logger import logging
from src.exception import MyException
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import accuracy_score , recall_score,precision_score,f1_score
from src.constants import MODEL_TRAINER_EXPECTED_SCORE
from src.entity.config_entity import ModelTrainerConfig
from src.entity.artifact_entity import ModelTrainerArtifact , ClasificationMetricArtifact , DataTransformationArtifact
from src.utils.main_utils import load_numpy_array_data, save_obj ,read_yaml_file , write_yaml_file

class ModelTraining:
      
      def __init__(self , model_trainer_config:ModelTrainerConfig , data_transformation_artifact:DataTransformationArtifact):
            try:
                self.model_trainer_config=model_trainer_config
                self.data_transformation_artifact=data_transformation_artifact
            except Exception as e:
                  raise MyException(e,sys) from e
            
      def train_model_from_scratch(self,x_train , y_train):
            try:

                  param_distributions = {
                      # 100 to 200 trees is plenty; 500 adds massive fit time for minimal gain
                      'n_estimators': [100, 150, 200],
                      
                      # Cap max_depth at 25 to prevent deep, slow tree generation
                      'max_depth': [10, 15, 20, 25],
                      
                      # Higher split thresholds speed up tree creation significantly
                      'min_samples_split': [5, 10],
                      
                      # Leaves >= 2 smooth decision boundaries and stop overfitting
                      'min_samples_leaf': [2, 4],
                      
                      # 'sqrt' is the standard gold standard for classification; skip None
                      'max_features': ['sqrt']
                  }
                  
                  rf_base = RandomForestClassifier(random_state=42, n_jobs=-1)
                  
                  random_search = RandomizedSearchCV(
                      estimator=rf_base,
                      param_distributions=param_distributions,
                      n_iter=10,             # Number of parameter combinations sampled
                      scoring='f1',          # Use 'f1', 'roc_auc', or 'precision' for imbalanced data
                      cv=5,                  # 5-fold cross-validation
                      verbose=2,
                      random_state=42,
                      n_jobs=-1,             # Use all available CPU cores
                      error_score='raise'
                  )
                  
                  logging.info("Starting RandomizedSearchCV hyperparameter tuning...")
                  model = random_search.fit(x_train, y_train)
                  logging.info("RandomizedSearchSv hyperparameter tuning over .!")
                  best_params = model.best_params_
                  logging.info(f"with best params - {best_params}")
                  
                  write_yaml_file(self.model_trainer_config.best_params_path,best_params)                  
                  logging.info("yaml file containing best params created ")
                  
                  return model.best_estimator_
            
            except Exception as e:
                  raise MyException(e,sys) from e
      
      def load_model_with_params(self,params,x_train ,y_train):
            rf_base = RandomForestClassifier( **params ,random_state=42, n_jobs=-1)
            model = rf_base.fit(x_train , y_train)
            return model

      def get_model_object_and_report(self,train:np.array,test:np.array):
            try:  
                  x_train, y_train, x_test, y_test = train[:, :-1], train[:, -1], test[:, :-1], test[:, -1]


                  if os.path.exists(self.model_trainer_config.best_params_path):
                        params = read_yaml_file(self.model_trainer_config.best_params_path)
                        model = self.load_model_with_params(params,x_train,y_train)
                  else:
                        os.makedirs(os.path.dirname(self.model_trainer_config.best_params_path) , exist_ok=True)
                        model = self.train_model_from_scratch(x_train,y_train)
                  
                  y_pred = model.predict(x_test)
                  accuracy = accuracy_score(y_test , y_pred)
                  f1 = f1_score(y_test , y_pred)
                  recall=recall_score(y_test , y_pred)
                  precision=precision_score(y_test , y_pred)
                  
                  metrics = ClasificationMetricArtifact(
                        accuracy = accuracy , f1_score = f1 , precision_score = precision , recall_score = recall
                  )
                  
                  return  model , metrics                 
                  
            except Exception as e:
                  raise MyException(e,sys) from e
      
      def initiate_model_trainer(self):
            
            try:
                train =  load_numpy_array_data(self.data_transformation_artifact.transformed_train_file_path)        
                test =  load_numpy_array_data(self.data_transformation_artifact.transformed_test_file_path)        
          
                trained_model , metrics = self.get_model_object_and_report(train,test)
                 
                save_obj(self.model_trainer_config.trained_model_file_path   , trained_model )
                write_yaml_file(self.model_trainer_config.metrics_file_path,metrics)
                
                if metrics.accuracy < MODEL_TRAINER_EXPECTED_SCORE:
                      logging.info('model accuracy below minimum threshold limit')
                      raise Exception("model accuracy below minimum threshold limit")
                
                model_trainer_artifact = ModelTrainerArtifact(
                      trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                      metric_artifact=metrics
                )
            
                return model_trainer_artifact
          
            except Exception as e:
                  raise MyException(e,sys) from e  
            
            
