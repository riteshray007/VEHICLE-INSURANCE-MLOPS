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
            
            
      