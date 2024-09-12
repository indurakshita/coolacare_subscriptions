SITE_URL = 'https://subscription.coolocare.com'

Q_CLUSTER = {
    'name': 'mycluster',
    'workers': 4,
    'recycle': 500,
    'timeout': 3600,  
    'retry': 5400, 
    'compress': True,
    'cpu_affinity': 1,
    'save_limit': 250,
    'queue_limit': 500,
    'redis': {
        'host': '35.168.103.206',
        'port': 6379,
        'db': 0,
        # 'password': 'CoolocareDB',
        'socket_timeout': 3,
        'retry_on_timeout': True,
    }
}

DATABASES = {
    'default': {
        'ENGINE':"django.db.backends.mysql",
        'NAME': 'coolocare',
        'USER': 'admin',
        'PASSWORD': 'NishubCoolocare',
        'HOST': 'database-1.cv2moc44u9pj.us-east-1.rds.amazonaws.com',
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'STRICT_ALL_TABLES',
        },
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
DESTINATIONPHONENUMBER = '+18336093526'
AWS_ACCESS_KEY = 'BKIA3ZHTIJMKTYREWZE3'
AWS_SECRET_KEY = 'P8/HnmrevfOjw2RIqT1v6Jlk32NRI1jGyHJZe4O8'
REGION_NAME = 'us-east-1'
CONTACT_FLOW_ID = 'bfffbab2-860d-4e71-bd2b-6f08b01d42af'
INSTANCE_ID = '7e6c7438-fe9a-4dc1-9616-0b7fcea0c715'