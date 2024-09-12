from typing import List
import random
import requests
import json
import datetime

def accucheck(bearer_token):
    
    high_value = random.randint(70, 300)

    request_data = {
    "deviceUnit": {
        "deviceId": 16,
        "imei":"60:E8:5B:69:3D:7A",
        "serialNumber":"60:E8:5B:69:3D:7A",
        "externalId":"60:E8:5B:69:3D:7A"
    },
    "vitalReadings": [
        {
        "dataId": "Blood Glucose",
        "highValue":high_value,
        "lowValue": 1,
        "collectionDate": datetime.datetime.utcnow().isoformat(), 
        "vitalId": 3
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

    print(f"accucheck: {response.text}")


if __name__ == "__main__":
    accucheck()