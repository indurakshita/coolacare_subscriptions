from typing import List
import random
import requests
import json
import datetime

def temp(bearer_token):
    
    low_value_celsius = random.randint(35, 42)
    high_value_fahrenheit = (low_value_celsius * 9/5) + 32

    request_data = {
    "deviceUnit": {
        "deviceId": 3,
        "imei":"C0:26:DA:0C:0A:95",
        "serialNumber":"C0:26:DA:0C:0A:95",
        "externalId":"C0:26:DA:0C:0A:95"
    },
    "vitalReadings": [
        {
        "dataId": "Temperature",
        "highValue":high_value_fahrenheit,
        "lowValue": low_value_celsius,
        "collectionDate": datetime.datetime.utcnow().isoformat(),  # Convert datetime to ISO format string
        "vitalId": 4
        }
    ]
    }

    # Convert the request data to a JSON string
    json_data = json.dumps(request_data)

    # Define the URL of the API endpoint
    url = "https://api.onecare.co/api/v2/rpm-service/vital-readings/new/"

    # Define the headers
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {bearer_token}',
        'User-Agent': 'MyApp/1.0',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'
    }

    # Send the POST request
    response = requests.post(url, headers=headers, data=json_data)

    # Print the response
    print(f"tempeture: {response.text}")
    
if __name__ == "__main__":
    temp()
