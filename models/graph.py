import os
from typing import List, Optional

def get_query(init_date: str, lat: float, lon: float, variables: Optional[List[str]] = None) -> str:
    """
    Returns the BigQuery SQL query for the WeatherNext Graph model.
    """

    all_variables = {
        "forecast_time": "forecast.time",
        "hours": "forecast.hours",
        "total_precipitation_6hr": "forecast.total_precipitation_6hr",
        "10m_u_component_of_wind": "forecast.u_component_of_wind_10m",
        "10m_v_component_of_wind": "forecast.v_component_of_wind_10m",
        "2m_temperature_celsius": "forecast.temperature_2m - 273.15",
        "mean_sea_level_pressure": "forecast.mean_sea_level_pressure",
        "50_geopotential": "forecast.geopotential_50",
        "100_geopotential": "forecast.geopotential_100",
        "150_geopotential": "forecast.geopotential_150",
        "200_geopotential": "forecast.geopotential_200",
        "250_geopotential": "forecast.geopotential_250",
        "300_geopotential": "forecast.geopotential_300",
        "400_geopotential": "forecast.geopotential_400",
        "500_geopotential": "forecast.geopotential_500",
        "600_geopotential": "forecast.geopotential_600",
        "700_geopotential": "forecast.geopotential_700",
        "850_geopotential": "forecast.geopotential_850",
        "925_geopotential": "forecast.geopotential_925",
        "1000_geopotential": "forecast.geopotential_1000",
        "50_specific_humidity": "forecast.specific_humidity_50",
        "100_specific_humidity": "forecast.specific_humidity_100",
        "150_specific_humidity": "forecast.specific_humidity_150",
        "200_specific_humidity": "forecast.specific_humidity_200",
        "250_specific_humidity": "forecast.specific_humidity_250",
        "300_specific_humidity": "forecast.specific_humidity_300",
        "400_specific_humidity": "forecast.specific_humidity_400",
        "500_specific_humidity": "forecast.specific_humidity_500",
        "600_specific_humidity": "forecast.specific_humidity_600",
        "700_specific_humidity": "forecast.specific_humidity_700",
        "850_specific_humidity": "forecast.specific_humidity_850",
        "925_specific_humidity": "forecast.specific_humidity_925",
        "1000_specific_humidity": "forecast.specific_humidity_1000",
        "50_temperature": "forecast.temperature_50",
        "100_temperature": "forecast.temperature_100",
        "150_temperature": "forecast.temperature_150",
        "200_temperature": "forecast.temperature_200",
        "250_temperature": "forecast.temperature_250",
        "300_temperature": "forecast.temperature_300",
        "400_temperature": "forecast.temperature_400",
        "500_temperature": "forecast.temperature_500",
        "600_temperature": "forecast.temperature_600",
        "700_temperature": "forecast.temperature_700",
        "850_temperature": "forecast.temperature_850",
        "925_temperature": "forecast.temperature_925",
        "1000_temperature": "forecast.temperature_1000",
        "50_u_component_of_wind": "forecast.u_component_of_wind_50",
        "100_u_component_of_wind": "forecast.u_component_of_wind_100",
        "150_u_component_of_wind": "forecast.u_component_of_wind_150",
        "200_u_component_of_wind": "forecast.u_component_of_wind_200",
        "250_u_component_of_wind": "forecast.u_component_of_wind_250",
        "300_u_component_of_wind": "forecast.u_component_of_wind_300",
        "400_u_component_of_wind": "forecast.u_component_of_wind_400",
        "500_u_component_of_wind": "forecast.u_component_of_wind_500",
        "600_u_component_of_wind": "forecast.u_component_of_wind_600",
        "700_u_component_of_wind": "forecast.u_component_of_wind_700",
        "850_u_component_of_wind": "forecast.u_component_of_wind_850",
        "925_u_component_of_wind": "forecast.u_component_of_wind_925",
        "1000_u_component_of_wind": "forecast.u_component_of_wind_1000",
        "50_v_component_of_wind": "forecast.v_component_of_wind_50",
        "100_v_component_of_wind": "forecast.v_component_of_wind_100",
        "150_v_component_of_wind": "forecast.v_component_of_wind_150",
        "200_v_component_of_wind": "forecast.v_component_of_wind_200",
        "250_v_component_of_wind": "forecast.v_component_of_wind_250",
        "300_v_component_of_wind": "forecast.v_component_of_wind_300",
        "400_v_component_of_wind": "forecast.v_component_of_wind_400",
        "500_v_component_of_wind": "forecast.v_component_of_wind_500",
        "600_v_component_of_wind": "forecast.v_component_of_wind_600",
        "700_v_component_of_wind": "forecast.v_component_of_wind_700",
        "850_v_component_of_wind": "forecast.v_component_of_wind_850",
        "925_v_component_of_wind": "forecast.v_component_of_wind_925",
        "1000_v_component_of_wind": "forecast.v_component_of_wind_1000",
        "50_vertical_velocity": "forecast.vertical_velocity_50",
        "100_vertical_velocity": "forecast.vertical_velocity_100",
        "150_vertical_velocity": "forecast.vertical_velocity_150",
        "200_vertical_velocity": "forecast.vertical_velocity_200",
        "250_vertical_velocity": "forecast.vertical_velocity_250",
        "300_vertical_velocity": "forecast.vertical_velocity_300",
        "400_vertical_velocity": "forecast.vertical_velocity_400",
        "500_vertical_velocity": "forecast.vertical_velocity_500",
        "600_vertical_velocity": "forecast.vertical_velocity_600",
        "700_vertical_velocity": "forecast.vertical_velocity_700",
        "850_vertical_velocity": "forecast.vertical_velocity_850",
        "925_vertical_velocity": "forecast.vertical_velocity_925",
        "1000_vertical_velocity": "forecast.vertical_velocity_1000",
    }

    if not variables:
        # Select all variables if none are specified
        select_clause = "\n".join([f"{v} as {k}" for k, v in all_variables.items()])
    else:
        # Select only the specified variables
        select_clause = "\n".join([f"{all_variables[v]} as {v}" for v in variables if v in all_variables])

    project_id = os.getenv("GCP_PROJECT_ID")
    table_id = f"{project_id}.weathernext_graph_forecasts.59572747_4_0"
    query = f"""
        SELECT
            {select_clause}
        FROM `{table_id}` AS wn_graph
        CROSS JOIN wn_graph.forecast AS forecast
        WHERE
            DATE(wn_graph.init_time) = DATE('{init_date}')
            AND ST_CONTAINS(wn_graph.geography_polygon, ST_GEOGPOINT({lon}, {lat}))
    """
    return query
