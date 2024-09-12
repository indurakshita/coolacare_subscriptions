from typing import List
import random
import requests
import json
import datetime

def manualoxygen(bearer_token):
    blood_oxygen_high_value = random.randint(90,100)
    request_data = {
        "vitalId": 7,
        "vitalReading": {
        "dataId": "Blood Oxygen",
        "highValue": blood_oxygen_high_value,
        "lowValue": 1,
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
    print(f"Manual blood oxygen: {response.text}")
        
    if __name__ == "__main__":
        manualoxygen()
