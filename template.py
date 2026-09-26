import os
from pathlib import Path

project_name = 'src'

list_of_files = [
      f"{project_name}/__init__.py",
      f"{project_name}/components/__init__.py",
      f"{project_name}/components/data_ingestion.py",
      f"{project_name}/components/data_validation.py",
      f"{project_name}/components/data_transformation.py",
      f"{project_name}/components/model_training.py",
      f"{project_name}/components/model_evaluation.py",
      f"{project_name}/components/model_pusher.py",
      f"{project_name}/logger/__init__.py",
      f"{project_name}/exception/__init__.py",
      f"{project_name}/constants/__init__.py",
      f"{project_name}/configuration/__init__.py",
      f"{project_name}/configuration/mongo_db_connection.py",
      f"{project_name}/configuration/aws_connection.py",
      f"{project_name}/data_access/__init__.py",
      f"{project_name}/data_access/proj1_data.py",
      f"{project_name}/entity/__init__.py",
      f"{project_name}/entity/artifact_entity.py",
      f"{project_name}/entity/config_entity.py",
      f"{project_name}/entity/estimator.py",
      f"{project_name}/entity/s3_estimator.py",
      f"{project_name}/pipeline/__init__.py",
      f"{project_name}/pipeline/prediction_pipeline.py",
      f"{project_name}/pipeline/training_pipeline.py",
      "app.py",
      "requirements.txt",
      "demo.py",
      "setup.py",
      "pyproject.toml",
]

for filepath in list_of_files:
      filepath = Path(filepath)
      filedir , filename = os.path.split(filepath)
      if filedir!='':
            os.makedirs(filedir , exist_ok=True)
      if ( not os.path.exists(filepath)) or (os.path.getsize(filepath)==0):
            with open(filepath , "w") as f:
                  pass
      else:
            print(f"file is already present at: {filepath}")
            
            
      