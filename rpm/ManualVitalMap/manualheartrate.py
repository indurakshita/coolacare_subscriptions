from typing import List
import random
import requests
import json
import datetime

def manualheartrate(bearer_token):
    heart_rate_high_value =random.randint(60,120)
    
    request_data = {
        "vitalId": 5,
        "vitalReading": {
        "dataId": "Heart Rate",
        "highValue": heart_rate_high_value,
        "lowValue": 1,
        "collectionDate": datetime.datetime.utcnow().isoformat(),
        }
        }

    json_data = json.dumps(request_data)
    url = "https://api.onecare.co/api/v2/rpm-service/vital-readings/manual/"

    # Define the headers
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {bearer_token}',
        'User-Agent': 'MyApp/1.0',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'
    }
    response = requests.post(url, headers=headers, data=json_data)

    print(f"Manual heart rate: {response.text}")
        
    if __name__ == "__main__":
        manualheartrate()
