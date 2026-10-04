from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse, RedirectResponse
from uvicorn import run as app_run

from typing import Optional

# Importing constants and pipeline modules from the project
from src.constants import APP_HOST, APP_PORT
from src.pipeline.prediction_pipeline import VehicleDataClassifier
from src.pipeline.training_pipeline import TrainPipeline
from src.logger import logging
from src.exception import MyException
import pandas as pd
import sys


# Initialize FastAPI application
app = FastAPI()

# Initialize the VehicleDataClassifier class so we dont have to 
# download the remote model from s3 every time someone hit predict 
model_predictor = VehicleDataClassifier()

# Mount the 'static' directory for serving static files (like CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 template engine for rendering HTML templates
templates = Jinja2Templates(directory='templates')

# Allow all origins for Cross-Origin Resource Sharing (CORS)
origins = ["*"]

# Configure middleware to handle CORS, allowing requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DataForm:
    """
    DataForm class to handle and process incoming form data.
    This class defines the vehicle-related attributes expected from the form.
    """
    def __init__(self, request: Request):
        self.request: Request = request
        self.Gender: Optional[str] = None
        self.Age: Optional[int] = None
        self.Driving_License: Optional[int] = None
        self.Region_Code: Optional[float] = None
        self.Previously_Insured: Optional[int] = None
        self.Annual_Premium: Optional[float] = None
        self.Policy_Sales_Channel: Optional[float] = None
        self.Vintage: Optional[int] = None
        self.Vehicle_Age: Optional[str] = None
        self.Vehicle_Damage: Optional[str] = None
                
                
    @classmethod
    async def from_request(cls, request: Request):
        instance = cls(request)
        await instance.get_vehicle_data()
        return instance
    
    def get_vehicle_input_data_frame(self):
        try:
            input_data = {
                "Gender": [self.Gender],
                "Age": [self.Age],
                "Driving_License": [self.Driving_License],
                "Region_Code": [self.Region_Code],
                "Previously_Insured": [self.Previously_Insured],
                "Vehicle_Age": [self.Vehicle_Age],
                "Vehicle_Damage": [self.Vehicle_Damage],
                "Annual_Premium": [self.Annual_Premium],
                "Policy_Sales_Channel": [self.Policy_Sales_Channel],
                "Vintage": [self.Vintage],
            }

            logging.info("Created vehicle data dataFrame")
            logging.info("Exited get_vehicle_input_data_frame method as DataForm class")
            return pd.DataFrame(input_data)

        except Exception as e:
            raise MyException(e, sys) from e
        
    async def get_vehicle_data(self):
        """
        Method to retrieve and assign form data to class attributes.
        This method is asynchronous to handle form data fetching without blocking.
        """
        form = await self.request.form()
        self.Gender = form.get("Gender")                 # "Female" or "Male"
        self.Age = int(form.get("Age"))
        self.Driving_License = int(form.get("Driving_License"))
        self.Region_Code = float(form.get("Region_Code"))
        self.Previously_Insured = int(form.get("Previously_Insured"))
        self.Vehicle_Age = form.get("Vehicle_Age")       # "< 1 Year", "1-2 Years", or "> 2 Years"
        self.Vehicle_Damage = form.get("Vehicle_Damage") # "Yes" or "No"
        self.Annual_Premium = float(form.get("Annual_Premium"))
        self.Policy_Sales_Channel = float(form.get("Policy_Sales_Channel"))
        self.Vintage = int(form.get("Vintage"))

# Route to render the main page with the form
@app.get("/", tags=["authentication"])
async def index(request: Request):
    """
    Renders the main HTML form page for vehicle data input.
    """
    return templates.TemplateResponse(
    request=request,
    name="vehicledata.html",
    context={"context": "Rendering"},
    )

# Route to trigger the model training process
# @app.get("/train")
# async def trainRouteClient():
#     """
#     Endpoint to initiate the model training pipeline.
#     """
#     try:
#         train_pipeline = TrainPipeline()
#         evalution_artifact = train_pipeline.run_pipeline()
        
#         if evalution_artifact.is_model_accepted:
#             model_predictor.refresh_model()
#             return Response("Training successful. Production model refreshed.")
        
#         return Response("Training successfull!!! but the trained model is not accepted ")
    

#     except Exception as e:
#         return Response(f"Error Occurred! {e}")

# Route to handle form submission and make predictions
@app.post("/")
async def predictRouteClient(request: Request):
    """
    Endpoint to receive form data, process it, and make a prediction.
    """
    try:
        # this is creating a instance of DataForm class and then 
        # form = DataForm(request)
        # here it is accessing the get_vehicle_data method of the form instance
        # this is one way of doing things
        # await form.get_vehicle_data()
        
        # the other way could be use an asynchronous class method:
        form = await DataForm.from_request(request) #does the job of above 2 lines
        
        # vehicle_data = VehicleData(
        #                         Gender= form.Gender,
        #                         Age = form.Age,
        #                         Driving_License = form.Driving_License,
        #                         Region_Code = form.Region_Code,
        #                         Previously_Insured = form.Previously_Insured,
        #                         Annual_Premium = form.Annual_Premium,
        #                         Policy_Sales_Channel = form.Policy_Sales_Channel,
        #                         Vintage = form.Vintage,
        #                         Vehicle_Age_lt_1_Year = form.Vehicle_Age_lt_1_Year,
        #                         Vehicle_Age_gt_2_Years = form.Vehicle_Age_gt_2_Years,
        #                         Vehicle_Damage_Yes = form.Vehicle_Damage_Yes
        #                         )

        # Convert form data into a DataFrame for the model
        vehicle_df = form.get_vehicle_input_data_frame()

        # model_predictor = VehicleDataClassifier()

        # Make a prediction and retrieve the result
        value = model_predictor.predict(dataframe=vehicle_df)[0]

        # Interpret the prediction result as 'Response-Yes' or 'Response-No'
        status = "Response-Yes" if value == 1 else "Response-No"

        # Render the same HTML page with the prediction result
        return templates.TemplateResponse(
            request= request,
            name = "vehicledata.html",
            context = { "context": status}
        )
        
    except Exception as e:
        return {"status": False, "error": f"{e}"}

# Main entry point to start the FastAPI server
if __name__ == "__main__":
    app_run(app, host=APP_HOST, port=APP_PORT)