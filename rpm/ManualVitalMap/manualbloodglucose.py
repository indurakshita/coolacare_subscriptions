import random
import requests
import json
import datetime

def manualglucose(bearer_token):
    
    high_value = random.randint(70, 300)
    
    request_data = {
        "vitalId": 3,
        "vitalReading": {
        "dataId": "Blood Glucose",
        "highValue": high_value,
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
    print(f"Manual blood glucose: {response.text}")
        
if __name__ == "__main__":
    manualglucose()
