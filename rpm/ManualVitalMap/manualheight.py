from typing import List
import random
import requests
import json
import datetime

def manualheight(bearer_token):
    low_value = round(random.uniform(1, 150), 2)  # Example range for low value, rounded to 2 decimal places
    high_value = round(random.uniform(151, 300), 2)
    
    request_data = {
        "vitalId": 6,
        "patientId": 0,
        "vitalReading": {
        "dataId": "Blood Oxygen",
        "highValue": 0,
        "lowValue": 0,
        "collectionDate": datetime.datetime.utcnow().isoformat(),
        }
        }

            # Convert the request data to a JSON string
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
    print(f"tempeture: {response.text}")
        
    if __name__ == "__main__":
        manualtemp()
