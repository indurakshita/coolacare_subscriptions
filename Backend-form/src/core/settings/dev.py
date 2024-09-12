from core.panel import *
from common.configs import ConfigParser

SITE_URL = "http://127.0.0.1:8000"

parser = ConfigParser(config_path="settings.database_settings")

DATABASES = parser.load(envs="default")

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
        'host': 'localhost',
        'port': 6379,
        'db': 0,
        'socket_timeout': 3,
        'retry_on_timeout': True,
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
DESTINATIONPHONENUMBER = '+18336093526'
AWS_ACCESS_KEY = 'BKIA3ZHTIJMKTYREWZE3'
AWS_SECRET_KEY = 'P8/HnmrevfOjw2RIqT1v6Jlk32NRI1jGyHJZe4O8'
REGION_NAME = 'us-east-1'
CONTACT_FLOW_ID = 'bfffbab2-860d-4e71-bd2b-6f08b01d42af'
INSTANCE_ID = '7e6c7438-fe9a-4dc1-9616-0b7fcea0c715'