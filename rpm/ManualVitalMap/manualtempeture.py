from typing import List
import random
import requests
import json
import datetime

def manualtemp(bearer_token):
    
    low_value_celsius = random.randint(35, 42)
    high_value_fahrenheit = (low_value_celsius * 9/5) + 32

    request_data = {
        "vitalId": 4,
        "vitalReading": {
        "dataId": "Temperature",
        "highValue": high_value_fahrenheit,
        "lowValue": low_value_celsius,
        "collectionDate": datetime.datetime.utcnow().isoformat(),
        }
        }

    json_data = json.dumps(request_data)
    url = "https://api.onecare.co/api/v2/rpm-service/vital-readings/manual/"
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {bearer_token}',
        'User-Agent': 'MyApp/1.0',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'
    }

    response = requests.post(url, headers=headers, data=json_data)
    print(f"Manual tempeture: {response.text}")
        
    if __name__ == "__main__":
        manualtemp()
