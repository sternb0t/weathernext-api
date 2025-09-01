import pytest
from fastapi.testclient import TestClient
from main import app
import pandas as pd
from unittest.mock import patch, MagicMock

client = TestClient(app)

@pytest.fixture
def mock_bigquery_client():
    with patch('main.client', new_callable=MagicMock) as mock_client:
        yield mock_client

def test_get_forecast_sorted(mock_bigquery_client):
    # Create a sample unsorted DataFrame
    data = {
        'forecast_time': pd.to_datetime(['2023-04-18T18:00:00+00:00', '2023-04-18T06:00:00+00:00', '2023-04-18T12:00:00+00:00']),
        '2m_temperature_celsius': [15.0, 10.0, 20.0]
    }
    unsorted_df = pd.DataFrame(data)

    # Configure the mock to return the unsorted DataFrame
    mock_query_job = MagicMock()
    mock_query_job.to_dataframe.return_value = unsorted_df
    mock_bigquery_client.query.return_value = mock_query_job

    # Make a request to the API
    response = client.get("/forecast?init_date=2023-04-18&lat=40.416775&lon=-3.703790&model=graph")

    # Check that the response is successful
    assert response.status_code == 200

    # Check that the forecast data is sorted by forecast_time
    forecast_data = response.json()['forecast']
    forecast_times = [item['forecast_time'] for item in forecast_data]
    assert forecast_times == sorted(forecast_times)
