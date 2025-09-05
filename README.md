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

## Example Notebook

An example of how to use this API in a Jupyter Notebook can be found in the `api_example_notebook.ipynb` file. This notebook can be run in Google Colab or a local Jupyter environment.

## Running Tests

To run the unit tests, run the following command from the root of the project:

```
virtualenv/bin/python3 -m pytest
```
