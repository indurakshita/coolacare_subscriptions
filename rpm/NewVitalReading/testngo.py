from typing import List
import random
import requests
import json
import datetime  # Import the datetime module

def testngo(bearer_token):
    
    high_value = random.randint(70, 300)
    
    request_data = {
    "deviceUnit": {
        "deviceId": 7,
        "imei":"C0:26:DA:01:29:97",
        "serialNumber":"C0:26:DA:01:29:97",
        "externalId":"C0:26:DA:01:29:97"
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

    json_data = json.dumps(request_data)
    url = "https://api.onecare.co/api/v2/rpm-service/vital-readings/new/"
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {bearer_token}',
        'User-Agent': 'MyApp/1.0',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'
    }

    response = requests.post(url, headers=headers, data=json_data)

    print(f"tetngo: {response.text}")

if __name__ == "__main__":
    testngo()