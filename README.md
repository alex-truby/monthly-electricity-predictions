# monthly-electricity-predictions
A small scale example project to predict monthly electricity consumption, complete with model, API, and docker deployment. 

## Goal
The goal of this repo is to build a small scale API endpoint that predicts the monthly electricity consumption of single-family homes in California. The endpoint takes in monthly average temperature along with relevant building characteristics, and returns the predicted monthly electricity consumption as an output. 

In `app.py`, you will find the scaffolding for a simple FastAPI app. Your task is to develop a prediction model and make it consumable through the `/consumption` endpoint.

## Contents
This repo contains setup and code for Earth Observation using Google Earth Engine (GEE) 
for water resources purposes in a Python editor environment.

    <monthly-electricity-predictiond>/
    ├─ api/                                  # contains app.py file for API deploment
    ├─ data/                                 # small scale datasets used for this project
    │  ├─ building_characteristics.parquet   # see 'Data Sources' section below
    │  ├─ electricity_consumption.parquet    # see 'Data Sources' section below
    │  ├─ temperature.parquet                # see 'Data Sources' section below
    ├─ eda/                                  # contains notebooks outlining EDA & model development
    ├─ models/                               # serialized models (ML)
    ├─ docker-compose.yaml                   # Docker configuration
    ├─ Dockerfile                            # Docker configuration
    ├─ pyproject.toml                        # pip install boilerplate
    ├─ requirements.txt                      # pip install boilerplate
    ├─ test_api.ipynb                        # notebook to test the api while running locally

## Data Sources
* `building_characteristics.parquet`: tabulates building characteristics for a sample of 3,978 single-family homes in California. Documentation for each characteristic can be found [here](https://resstock.readthedocs.io/en/latest/workflow_inputs/characteristics.html)

* `temperature.parquet`: contains the daily average temperatures for every county in California. The timespan of the data is from 2018-01-01 to 2018-12-31.

* `electricity_consumption.parquet`: contains the daily electricity consumption in kWh for all buildings in `building_characteristics.parquet`. The timespan of the data is from 2018-01-01 to 2018-12-31.

## Running the API
If you have docker desktop installed, simply run the following command from within this directory:
```bash
docker-compose up --build --force-recreate
```

Otherwise, run the following command from within this directory:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
uvicorn api.app:app --reload
```

The API will be accessible at `http://localhost:8000`. 
