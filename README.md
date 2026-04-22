# WeatherNext API

This is a simple Python API to access WeatherNext forecasting datasets stored in BigQuery.


[![Open in Cloud Shell](https://gstatic.com/cloudssh/images/open-btn.svg)](https://shell.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https://github.com/sternb0t/weathernext-api.git)


## Setup

1.  **Install dependencies:**

    ```
    pip install -r requirements.txt
    ```

2.  **Set up your environment:**

    Create a `.env` file in the root of the project and add your GCP Project ID:

    ```
    GCP_PROJECT_ID="your-gcp-project-id"
    ```

3.  **Authenticate with Google Cloud:**

    Make sure you have the `gcloud` CLI installed and authenticated:

    ```
    gcloud auth application-default login
    ```

## Running the API

1.  **Start the server:**

    ```
    uvicorn main:app --reload
    ```

2.  **Access the API documentation:**

    Once the server is running, you can access the interactive API documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## Example Request

```
curl -X 'GET' \
  'http://127.0.0.1:8000/forecast?init_date=2023-04-18&lat=40.416775&lon=-3.703790&model=gfs&variables=temperature_2m_above_ground,total_precipitation_surface' \
  -H 'accept: application/json'
```

## API Response Format

A successful request returns a JSON object with the following structure:

```json
{
  "init_date": "2023-04-18",
  "latitude": 40.416775,
  "longitude": -3.703790,
  "model": "gfs",
  "forecast": [
    {
      "forecast_time": "2023-04-18T00:00:00Z",
      "temperature_2m_above_ground": 15.2,
      "total_precipitation_surface": 0.0
    },
    {
      "forecast_time": "2023-04-18T01:00:00Z",
      "temperature_2m_above_ground": 14.8,
      "total_precipitation_surface": 0.1
    }
  ]
}
```

### Response Fields

- **init_date**: The forecast initialization date (YYYY-MM-DD format)
- **latitude**: The requested latitude coordinate
- **longitude**: The requested longitude coordinate
- **model**: The forecast model used ('graph', 'gen', or 'gfs')
- **forecast**: Array of forecast records, each containing:
  - **forecast_time**: ISO 8601 timestamp of the forecast time
  - **[variable_name]**: Requested weather variables with their values (e.g., temperature_2m_above_ground, total_precipitation_surface)

### Error Responses

If a request fails, the API returns an error with an appropriate HTTP status code:

- **400 Bad Request**: Invalid parameters (invalid model, date format, or coordinates outside valid ranges)
- **404 Not Found**: No forecast data available for the specified date and location
- **500 Internal Server Error**: Backend error while fetching data from BigQuery

Error responses include a detail message explaining the issue.

## Example Notebook

An example of how to use this API in a Jupyter Notebook can be found in the `api_example_notebook.ipynb` file. This notebook can be run in Google Colab or a local Jupyter environment.

## Running Tests

To run the unit tests, run the following command from the root of the project:

```
virtualenv/bin/python3 -m pytest
```
