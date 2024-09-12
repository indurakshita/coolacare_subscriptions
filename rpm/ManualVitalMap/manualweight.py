from typing import List
import random
import requests
import json
import datetime

def manualweight(bearer_token):
    weight_high_value = random.randint(60,100)
    
    request_data = {
        "vitalId": 2,
        "vitalReading": {
        "dataId": "Weight",
        "highValue": weight_high_value,
        "lowValue": 1,
        "collectionDate": datetime.datetime.utcnow().isoformat(),
        }
        }

    json_data = json.dumps(request_data)

    # Define the URL of the API endpoint
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

    # Send the POST request
    response = requests.post(url, headers=headers, data=json_data)

    # Print the response
    print(f"Manual weight: {response.text}")
        
    if __name__ == "__main__":
        manualweight()
