from fastapi import FastAPI, HTTPException
from google.cloud import bigquery
from dotenv import load_dotenv
import os
import logging
import pandas as pd
import numpy as np
from functools import lru_cache
from datetime import datetime
from models import graph, gen, gfs
from typing import Optional

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="WeatherNext API",
    description="Access WeatherNext forecasting datasets from BigQuery.",
    version="1.0.0",
)

# Initialize BigQuery client (deferred to startup so tests can mock it)
project_id = os.getenv("GCP_PROJECT_ID")
client = None

@app.on_event("startup")
def _init_bigquery_client():
    global client
    client = bigquery.Client(project=project_id)

# Model mapping
models = {
    "graph": graph,
    "gen": gen,
    "gfs": gfs,
}

@lru_cache(maxsize=128)
def _fetch_forecast(query: str):
    query_job = client.query(query)
    df = query_job.to_dataframe()
    if df.empty:
        return None
    if 'forecast_time' in df.columns:
        df = df.sort_values(by='forecast_time').reset_index(drop=True)
    df = df.replace({np.nan: None})
    return df.to_dict(orient='records')

@app.get("/forecast")
def get_forecast(init_date: str, lat: float, lon: float, model: str = 'graph', variables: Optional[str] = None):
    """
    Get weather forecast for a specific date and location.

    - **init_date**: Forecast initialization date (YYYY-MM-DD).
    - **lat**: Latitude of the location (-90 to 90).
    - **lon**: Longitude of the location (-180 to 180).
    - **model**: Type of forecast model ('graph', 'gen', 'gfs').
    - **variables**: Comma-separated list of variables to return.
    """

    if model not in models:
        raise HTTPException(status_code=400, detail=f"Invalid model type. Available models are: {list(models.keys())}")

    try:
        datetime.strptime(init_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid init_date format. Use YYYY-MM-DD.")

    if not (-90 <= lat <= 90):
        raise HTTPException(status_code=400, detail="lat must be between -90 and 90.")
    if not (-180 <= lon <= 180):
        raise HTTPException(status_code=400, detail="lon must be between -180 and 180.")

    variable_list = tuple(variables.split(',')) if variables else None

    try:
        query = models[model].get_query(init_date, lat, lon, variable_list)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        records = _fetch_forecast(query)
    except Exception as e:
        logger.error("BigQuery error: %s", e)
        raise HTTPException(status_code=500, detail="An error occurred while fetching forecast data.")

    if records is None:
        raise HTTPException(status_code=404, detail="No forecast data found for the specified date and location.")

    return {
        "init_date": init_date,
        "latitude": lat,
        "longitude": lon,
        "model": model,
        "forecast": records,
    }
