from pathlib import Path
from urllib.parse import quote
from dotenv import load_dotenv
import os


load_dotenv()
KEY = os.getenv('KEY')


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = KEY
#ALLOWED_HOSTS = get_env("ALLOWED_HOSTS").split(",")
ALLOWED_HOSTS = ['localhost','127.0.0.1','0.0.0.0', 'studyways.ir']


CORS_REPLACE_HTTPS_REFERER = True
CORS_ALLOW_CREDENTIALS = True
# END CORSHEADERS CONFIGURATION
DEBUG = os.getenv("DEBUG") == "True"

JWT_SECRET = os.getenv("JWT_SECRET", default=SECRET_KEY)



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SITE_ID = 2

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/



if os.getenv("STAGE") == "PRODUCTION":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": os.getenv("POSTGRES_DB"),
            "USER": os.getenv("POSTGRES_USER"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
            "HOST": "sabalan.liara.cloud",
            "PORT": 33741,
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }



# APP CONFIGURATION
DJANGO_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "django.contrib.admindocs",
    "django.contrib.sites",
)

THIRD_PARTY_APPS = (
    "rest_framework",
    "django_filters",
    "corsheaders",
    "gunicorn",
    "whitenoise",
    "ckeditor",
    "ckeditor_uploader",
    "import_export",
    "storages",
    "rest_framework_swagger",
    "drf_yasg",
    "oauth2_provider",
    "social_django",
    "drf_social_oauth2",
)

# Apps specific for this project go here.

LOCAL_APPS = (
    "accounts",
    "file",
    "subscription",
    "blog",
    "service",
)


INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
# END APP CONFIGURATION

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates/",
        ],
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

WSGI_APPLICATION = "config.wsgi.application"


ACCOUNT_EMAIL_VERIFICATION = "none"


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation"
            ".UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.NumericPasswordValidator"
        ),
    },
]
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]




# S3 Settings
LIARA_ENDPOINT="https://storage.iran.liara.space"
LIARA_BUCKET_NAME="studyways"
LIARA_ACCESS_KEY="irgq6egfseolt7e4"
LIARA_SECRET_KEY="4154e712-daf4-4dbe-97a3-38c2a773a2cb"

# S3 Settings Based on AWS (optional)
AWS_ACCESS_KEY_ID = LIARA_ACCESS_KEY
AWS_SECRET_ACCESS_KEY = LIARA_SECRET_KEY
AWS_STORAGE_BUCKET_NAME = LIARA_BUCKET_NAME
AWS_S3_ENDPOINT_URL = LIARA_ENDPOINT
AWS_S3_REGION_NAME = 'us-east-1'


# Django-storages configuration
STORAGES = {
  "default": {
      "BACKEND": "storages.backends.s3.S3Storage",
  },
  "staticfiles": {
      "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
  },
}

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'



# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Tehran"
USE_I18N = True
USE_TZ = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_ROOT = os.getenv("STATIC_ROOT", default="/static/")
STATIC_URL = os.getenv("STATIC_URL", default="/static/")
MEDIA_ROOT = "https://studyways.storage.iran.liara.space/media/"
MEDIA_URL = "https://studyways.storage.iran.liara.space/media/"
#STATICFILES_DIRS = ["docs/"]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# CACHING CONFIGURATION
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://:lz8w2ZIVDIt8z3Mu4iJGvKS3@sabalan.liara.cloud:30854/0"
    }
}
# END CACHING CONFIGURATION




# AUTH USER MODEL CONFIGURATION
AUTH_USER_MODEL = "accounts.User"
# END AUTH USER MODEL CONFIGURATION

# OTP CONFIGURATION
OTP_CODE_LENGTH = int(os.getenv("OTP_CODE_LENGTH", default="4"))
OTP_TTL = int(os.getenv("OTP_TTL", default="120"))
# END OTP CONFIGURATION

# JWT SETIINGS
ACCESS_TTL = int(os.getenv("ACCESS_TTL", default="1"))  # days
REFRESH_TTL = int(os.getenv("REFRESH_TTL", default="2"))  # days
# END JWT SETTINGS




'''
AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',
    'drf_social_oauth2.backends.DjangoOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]
'''

# Google Configuration
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = "366111965494-bbgflimp8s9dtndoufsah3v235bt8lhh.apps.googleusercontent.com"
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = "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"
SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI = 'https://api.studyways.com/google-redirect/'
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
]




# REST FRAMEWORK CONFIGURATION
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "accounts.backends.JWTAuthentication",
        #"rest_framework.authentication.TokenAuthentication",
        #"rest_framework.authentication.SessionAuthentication",
        #"oauth2_provider.contrib.rest_framework.OAuth2Authentication",
        #"drf_social_oauth2.authentication.SocialAuthentication",
    ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    "DEFAULT_THROTTLE_RATES": {"otp": os.getenv("OTP_THROTTLE_RATE", default="10/min"), },
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# END REST FRAMEWORK CONFIGURATION

MAX_UPLOAD_SIZE = 5242880

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Format', 'Font', 'FontSize'],
            ['Bold', 'Italic'],
            ['TextColor', 'BGColor'],
            ['NumberedList', 'BulletedList'],
            ['Image', 'Flash', 'Table'],
            ['Source']
        ],
        'height': 100,
        'width': 650
    }
}

# CORSHEADERS CONFIGURATION
ALLOWED_HOSTS = ['studyways.ir','localhost','127.0.0.1','0.0.0.0', 'liara.run','app.studyways.ir']
CORS_ALLOWED_ORIGINS = ["https://app.studyways.ir","https://liara.run","http://localhost","http://127.0.0.1","https://studyways.ir","https://.liara.run","https://.studyways.ir"]
CSRF_TRUSTED_ORIGINS = ["https://app.studyways.ir","https://liara.run","http://localhost","http://127.0.0.1","https://studyways.ir","https://.liara.run","https://.studyways.ir"]
CORS_ORIGIN_ALLOW_ALL = True
CORS_REPLACE_HTTPS_REFERER = True
CORS_ALLOW_CREDENTIALS = True
SESSION_COOKIE_SECURE=True
#CSRF_COOKIE_SECURE = False
#CSRF_COOKIE_HTTPONLY = False
#SESSION_COOKIE_SAMESITE = False
#SESSION_COOKIE_DOMAIN = "http://195.214.235.46"
CORS_ORIGIN_WHITELIST = ["https://app.studyways.ir","https://liara.run","http://localhost","http://127.0.0.1","https://studyways.ir","https://.liara.run","https://.studyways.ir"]
# END CORSHEADERS CONFIGURATION



# SMS CONFIGURATION
KAVENEGAR_API_KEY = "7572365451704156594870726D765276525A7468646D553857503161754D683669545A6D755748517658383D"
KAVENEGAR_TEMPLATE = "otp-verify"
# END SMS CONFIGURATION

APPEND_SLASH = True


# ZARRINPAL CONFIGURATION
SANDBOX = True
ZARRINPAL_URL="https://api.zarinpal.com/pg/"
ZARRINPAL_MERCHANT_ID = "00000000-0000-0000-0000-000000000000"
ZP_API_REQUEST = "https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = "https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = "https://sandbox.zarinpal.com/pg/StartPay/"
ZARIN_CALL_BACK = 'https://api.studyways.ir/subscription/pay-verify/'
# END ZARRINPAL CONFIGURATION
