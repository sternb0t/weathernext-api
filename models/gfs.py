from typing import List, Optional

def get_query(init_date: str, lat: float, lon: float, variables: Optional[List[str]] = None) -> str:
    """
    Returns the BigQuery SQL query for the NOAA GFS model.
    """

    all_variables = {
        "forecast_time": "f.time",
        "hours": "f.hours",
        "temperature_2m_above_ground": "f.temperature_2m_above_ground",
        "specific_humidity_2m_above_ground": "f.specific_humidity_2m_above_ground",
        "relative_humidity_2m_above_ground": "f.relative_humidity_2m_above_ground",
        "u_component_of_wind_10m_above_ground": "f.u_component_of_wind_10m_above_ground",
        "v_component_of_wind_10m_above_ground": "f.v_component_of_wind_10m_above_ground",
        "total_precipitation_surface": "f.total_precipitation_surface",
        "precipitable_water_entire_atmosphere": "f.precipitable_water_entire_atmosphere",
        "total_cloud_cover_entire_atmosphere": "f.total_cloud_cover_entire_atmosphere",
        "downward_shortwave_radiation_flux": "f.downward_shortwave_radiation_flux",
    }

    if not variables:
        # Select all variables if none are specified
        select_clause = ",\n".join([f"{v} as {k}" for k, v in all_variables.items()])
    else:
        # Select only the specified variables
        select_clause = ",\n".join([f"{all_variables[v]} as {v}" for v in variables if v in all_variables])

    table_id = "bigquery-public-data.noaa_global_forecast_system.NOAA_GFS0P25"
    query = f"""
        SELECT
            {select_clause}
        FROM `{table_id}`,
             UNNEST(forecast) AS f
        WHERE
            DATE(creation_time) = DATE('{init_date}')
            AND ST_CONTAINS(geography_polygon, ST_GEOGPOINT({lon}, {lat}))
    """
    return query
