from typing import List
from pydantic import BaseModel, Field
from fastapi import FastAPI, Query, HTTPException
from starlette.responses import RedirectResponse
import joblib
import pandas as pd
from models.preprocessing import * 

# load pre-trained model
# first model did not have grid search implemented - RMSE of ~11.25
# model = joblib.load("./models/electricity_consumption_prototype_model.pkl")

# went back and implement a parameter grid search for the random forest model
model = joblib.load("./models/electricity_consumption_prototype_model_v2.pkl")



app = FastAPI(
    title='Monthly Electricity Consumption API',
    debug=True,
)

# Define the input schema using Pydantic
# could be used to validate params in GET request or in POST model if passing sensitive info
# use in conjunction with Depends() to inject the BaseModel as a dependency that pulls the query 
# parameters from the request URL
class ConsumptionInput(BaseModel):
    Average_Temperature: float
    Heating_setpoint: str
    Cooling_setpoint: str
    Vintage: str
    Floor_Area_SqFt: str
    Bedrooms: str
    Geometry_Stories: str
    Occupants: str
    ASHRAE_IECC_Climate_Zone_2004: str
    Windows: str
    Insulation_Wall: str
    Insulation_Roof: str
    Insulation_Floor: str
    HVAC_Heating_Fuel: str
    Roof_Material: str
    Water_Heater_Efficiency: str


@app.get("/")
def read_root():
    return RedirectResponse(url='/docs')

# One interesting update here might be to enot have ALL of the inputs be required
# could build out simple classifications models to predict missing "required" inputs
# for example, if a user does not know the roof insulation type, can we predict this based on
# location, year built, size, etc.




@app.get("/consumption")
def get_consumption(
    Average_Temperature: float,
    Heating_setpoint: str,
    Cooling_setpoint: str,
    Vintage: str,
    Floor_Area_SqFt: str,
    Occupants: str,
    ASHRAE_IECC_Climate_Zone_2004: str,
    Windows: str,
    Insulation_Wall: str,
    Insulation_Roof: str,
    Insulation_Floor: str,
    HVAC_Heating_Fuel: str,
    Roof_Material: str,
    Water_Heater_Efficiency: str,
):
    
    floor_area_sqft = transform_string_to_int(Floor_Area_SqFt)

    vintage = transform_vintage(Vintage)
    occupants = transform_occupants(Occupants)
    cooling_set_point = transform_set_point(Cooling_setpoint)
    heating_set_point = transform_set_point(Heating_setpoint)

    temperature_deviation = calculate_temperature_deviation(
        Average_Temperature, 
        heating_set_point, 
        cooling_set_point
    )

    # Create a DataFrame from the input
    input_data = pd.DataFrame([{
        "temp_deviation": temperature_deviation,
        "Vintage": vintage,
        "Floor Area SqFt": floor_area_sqft,
        "Occupants": occupants,
        "ASHRAE IECC Climate Zone 2004": ASHRAE_IECC_Climate_Zone_2004,
        "Windows": Windows,
        "Insulation Wall": Insulation_Wall,
        "Insulation Roof": Insulation_Roof,
        "Insulation Floor": Insulation_Floor,
        "HVAC Heating Fuel": HVAC_Heating_Fuel,
        "Roof Material": Roof_Material,
        "Water Heater Efficiency": Water_Heater_Efficiency
    }])

    # Ensure the input matches the model's expected format
    try:
        prediction = model.predict(input_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")

    # Return the prediction as a JSON response
    return {"predicted_consumption_kwh": prediction[0]}



# given lat lon of specific building, based on that - using data we already have, connect that to our best guess on an estimate

# load in geojson w/ geopandas
# need to join that lat/lons - need to check that those are in float format, and check that they are valid
# datum checks

# connect with existing data;
# group by county, get some insights as to dominant building features in that county
# build a small classification model based on the county (derived from joining lat lon with geojson), to determine the building features needed for model hosted in the app
# if lat lon if close to a border of the county


@app.get("/consumption")
def get_consumption(
    Average_Temperature: float,
    lat: float,
    lon: float

    # Heating_setpoint: str,
    # Cooling_setpoint: str,
    # Vintage: str,
    # Floor_Area_SqFt: str,
    # Occupants: str,
    # ASHRAE_IECC_Climate_Zone_2004: str,
    # Windows: str,
    # Insulation_Wall: str,
    # Insulation_Roof: str,
    # Insulation_Floor: str,
    # HVAC_Heating_Fuel: str,
    # Roof_Material: str,
    # Water_Heater_Efficiency: str,
):
    
    # method/function that takes in lat lon and outputs valid county id

    temperature_deviation = calculate_temperature_deviation(
        Average_Temperature, 
        heating_set_point, 
        cooling_set_point
    )

    county_id = get_county_from_lat_lon(lat, lon)

    # query "most common" building attributes for releant county
    # have a function where pass in that county_id

    # def get_most_common(featurea, featuresb):
    #     return mode from building dataset


    # Create a DataFrame from the input
    input_data = pd.DataFrame([{
        "temp_deviation": temperature_deviation,
        "Vintage": vintage,
        "Floor Area SqFt": floor_area_sqft,
        "Occupants": occupants,
        "ASHRAE IECC Climate Zone 2004": ASHRAE_IECC_Climate_Zone_2004,
        "Windows": Windows,
        "Insulation Wall": Insulation_Wall,
        "Insulation Roof": Insulation_Roof,
        "Insulation Floor": Insulation_Floor,
        "HVAC Heating Fuel": HVAC_Heating_Fuel,
        "Roof Material": Roof_Material,
        "Water Heater Efficiency": Water_Heater_Efficiency
    }])

    # Ensure the input matches the model's expected format
    try:
        prediction = model.predict(input_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")

    # Return the prediction as a JSON response
    return {"predicted_consumption_kwh": prediction[0]}