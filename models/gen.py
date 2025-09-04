import os
from typing import List, Optional

def get_query(init_date: str, lat: float, lon: float, variables: Optional[List[str]] = None) -> str:
    """
    Returns the BigQuery SQL query for the WeatherNext Gen model.
    """

    all_variables = {
        "forecast_time": "forecast.time",
        "hours": "forecast.hours",
        "ensemble_member": "ensemble.ensemble_member",
        "total_precipitation_12hr": "ensemble.total_precipitation_12hr",
        "100m_u_component_of_wind": "ensemble.u_component_of_wind_100m",
        "100m_v_component_of_wind": "ensemble.v_component_of_wind_100m",
        "10m_u_component_of_wind": "ensemble.u_component_of_wind_10m",
        "10m_v_component_of_wind": "ensemble.v_component_of_wind_10m",
        "2m_temperature_celsius": "ensemble.temperature_2m - 273.15",
        "mean_sea_level_pressure": "ensemble.mean_sea_level_pressure",
        "sea_surface_temperature": "ensemble.sea_surface_temperature",
    }

    if not variables:
        # Select all variables if none are specified
        select_clause = ",\n".join([f"{v} as {k}" for k, v in all_variables.items()])
    else:
        # Select only the specified variables
        select_clause = ",\n".join([f"{all_variables[v]} as {v}" for v in variables if v in all_variables])

    project_id = os.getenv("GCP_PROJECT_ID")
    table_id = f"{project_id}.weathernext_gen_forecasts.126478713_1_0"
    query = f"""
        SELECT
            {select_clause}
        FROM `{table_id}` AS wn_gen
        CROSS JOIN wn_gen.forecast AS forecast
        CROSS JOIN forecast.ensemble AS ensemble
        WHERE
            DATE(wn_gen.init_time) = DATE('{init_date}')
            AND ST_CONTAINS(wn_gen.geography_polygon, ST_GEOGPOINT({lon}, {lat}))
    """
    return query
