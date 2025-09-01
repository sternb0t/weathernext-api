from fastapi import FastAPI, HTTPException, Query
from google.cloud import bigquery
from dotenv import load_dotenv
import os
import pandas as pd
import numpy as np
from models import graph, gen, gfs
from typing import List, Optional

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="WeatherNext API",
    description="Access WeatherNext forecasting datasets from BigQuery.",
    version="1.0.0",
)

# Initialize BigQuery client
project_id = os.getenv("GCP_PROJECT_ID")
client = bigquery.Client(project=project_id)

# Model mapping
models = {
    "graph": graph,
    "gen": gen,
    "gfs": gfs,
}

@app.get("/forecast")
def get_forecast(init_date: str, lat: float, lon: float, model: str = 'graph', variables: Optional[str] = None):
    """
    Get weather forecast for a specific date and location.

    - **init_date**: Forecast initialization date (YYYY-MM-DD).
    - **lat**: Latitude of the location.
    - **lon**: Longitude of the location.
    - **model**: Type of forecast model ('graph', 'gen', 'gfs').
    - **variables**: Comma-separated list of variables to return.
    """

    if model not in models:
        raise HTTPException(status_code=400, detail=f"Invalid model type. Available models are: {list(models.keys())}")

    variable_list = variables.split(',') if variables else None

    # Get the query from the selected model
    query = models[model].get_query(init_date, lat, lon, variable_list)

    try:
        query_job = client.query(query)
        df = query_job.to_dataframe()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if df.empty:
        raise HTTPException(status_code=404, detail="No forecast data found for the specified date and location.")

    # Sort the dataframe by forecast_time
    if 'forecast_time' in df.columns:
        df = df.sort_values(by='forecast_time').reset_index(drop=True)

    # Replace NaN with None for JSON compatibility
    df = df.replace({np.nan: None})

    # Convert dataframe to JSON
    return {
        "init_date": init_date,
        "latitude": lat,
        "longitude": lon,
        "model": model,
        "forecast": df.to_dict(orient='records')
    }
