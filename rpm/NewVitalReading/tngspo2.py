import requests
import json
import datetime
import random  

def tngspo2(bearer_token):
    
    blood_oxygen_high_value = random.randint(90,100)

    heart_rate_high_value =random.randint(60,120)

    request_data = {
        "deviceUnit": {
            "deviceId": 5,
            "imei": "C0:26:DA:01:29:97",
            "serialNumber": "C0:26:DA:01:29:97",
            "externalId": "C0:26:DA:01:29:97"
        },
        "vitalReadings": [
            {
                "dataId": "Blood Oxygen",
                "highValue": blood_oxygen_high_value,
                "lowValue": 1,
                "collectionDate": datetime.datetime.utcnow().isoformat(),
                "vitalId": 7
            },
            {
                "dataId": "Heart Rate",
                "highValue": heart_rate_high_value,
                "lowValue": 1,
                "collectionDate": str(datetime.datetime.now()), 
                "vitalId": 5
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
    print(f"tngspo2: {response.text}")

if __name__ == "__main__":
    tngspo2()
