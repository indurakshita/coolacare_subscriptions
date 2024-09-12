import requests
import json
import datetime
import random  

def weight(bearer_token):

    weight_high_value = random.randint(60,100)
    request_data = {
        "deviceUnit": {
            "deviceId": 4,
            "imei": "C0:26:DA:01:29:97",
            "serialNumber": "C0:26:DA:01:29:97",
            "externalId": "C0:26:DA:01:29:97"
        },
        "vitalReadings": [
            {
                "dataId": "Weight",
                "highValue": weight_high_value,
                "lowValue": 1,
                "collectionDate": datetime.datetime.utcnow().isoformat(),
                "vitalId": 2
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
    print(f"weight: {response.text}")

if __name__ == "__main__":
    weight()
