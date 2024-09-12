import os
from pathlib import Path
from core.panel import *

BASE_DIR = Path(__file__).resolve().parent.parent.parent
BASE_DIR_PR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


EMAIL_TEMPLATE_DIR = "authapp/template"


SECRET_KEY = "django-insecure-k86l+k^ehizez#3y(gh)=if0&gd-ef&84zxe+po-t#lgq!+#$^"

DEBUG = True

ENVIRON = "develop"

ALLOWED_HOSTS = ["*"]

SESSION_COOKIE_AGE = 3600

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

CORS_ORIGIN_ALLOW_ALL = True  # Set to True to allow all origins, or specify specific origins

INSTALLED_APPS = [
    'corsheaders',
    "jazzmin",
    "django_extensions",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'django_filters',
    #third party packages
    "rest_framework",
    'easyaudit',
    "django_q",
    # 'django_otp',
    # 'django_otp.plugins.otp_totp',

    # 'drf_spectacular',


    # Apps
    "common",
    'authapp.apps.AuthappConfig',
    'confapp.apps.ConfappConfig',
    'subscription.apps.SubscriptionConfig',

    
]



MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'easyaudit.middleware.easyaudit.EasyAuditMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # "django_otp.middleware.OTPMiddleware",
    "common.middlewares.UserDataMiddleware",
    "djangorestframework_camel_case.middleware.CamelCaseMiddleWare",
]




ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR_PR,EMAIL_TEMPLATE_DIR)],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


WSGI_APPLICATION = "core.wsgi.application"

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': [
    ],
    "DEFAULT_RENDERER_CLASSES": (
        "djangorestframework_camel_case.render.CamelCaseJSONRenderer",
        "djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer",
    ),
    "DEFAULT_PARSER_CLASSES": (
        "djangorestframework_camel_case.parser.CamelCaseFormParser",
        "djangorestframework_camel_case.parser.CamelCaseMultiPartParser",
        "djangorestframework_camel_case.parser.CamelCaseJSONParser",
    ),
    "JSON_UNDERSCOREIZE": {
        "no_underscore_before_number": True,
    },
    "DEFAULT_PAGINATION_CLASS": "common.utils.Pagination",
    "EXCEPTION_HANDLER": "common.exceptions.ExceptionHandler.handle_exception",
    "DEFAULT_PAGINATION_CLASS": "common.utils.Pagination",
    "PAGE_SIZE": 10,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}


SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'


STRIPE_PUBLIC_KEY = 'pk_test_51O9f4UJ1bSMBsaCLof8awG0vtI9N0ouuhLi9phsX6MUcDMGq2vrTjIQYmBmufrIaZsRriqwb10qG2zjcqDpefQB600jsIfa1qn'
STRIPE_SECRET_KEY = 'sk_test_51O9f4UJ1bSMBsaCL3rAa9ADjg7TQarJTAvf91TM1rnPdNS7oc3RF7qe4g0gOzTN6VfwPCMeOdPAtF6ILRNt3yH3j002siOKgHE'



SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

SPECTACULAR_SETTINGS = {
    'TITLE': 'NISHUB API END POINTS ',
    'DESCRIPTION': '',
    'VERSION': '3.0.0',
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
    },
}


AUTH_USER_MODEL = 'authapp.CustomUser'

AUTHENTICATION_BACKENDS = [
    'authapp.backends.CustomUserModelBackend',
    
]


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(os.path.join(BASE_DIR, "static"))
STATICFILES_DIRS = [os.path.join(BASE_DIR, "staticdir")]

