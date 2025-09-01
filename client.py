import requests

# API endpoint URL
url = "http://127.0.0.1:8000/forecast"

# Parameters for the request (Madrid, Spain)
params = {
    "init_date": "2023-04-18",
    "lat": 40.416775,
    "lon": -3.703790,
    "model": "gfs",
    "variables": "temperature_2m_above_ground,total_precipitation_surface"
}

try:
    # Make the GET request
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Print the JSON response
        print(response.json())
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

except requests.exceptions.ConnectionError as e:
    print(f"Connection Error: {e}")
