from pathlib import Path
import environ
import os

env = environ.Env(
    DEBUG=(bool, False)
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env('SECRET_KEY')
SECRET_KEY = ''

DEBUG = env('DEBUG')

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #Mening applarim
    'users',
    'courses',
    'groups',
    'lessons',
    'homeworks',
    'exams',
    'attendance',
    'payments',
    'gamification',
    'shop',
    'branches',

    #Third party applar
    'django_filters',
    'rest_framework',
    'storages'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [f"{BASE_DIR+'templates/'}"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
        'OPTIONS': {
            'sslmode': env('DB_SSLMODE'),
        },
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR+"/static/",
]

LOGIN_REDIRECT_URL = 'listing:list'
LOGOUT_REDIRECT_URL = 'listing:list'

AUTH_USER_MODEL = 'users.User'

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR+"/media/"


SUPABASE_PROJECT_ID = env('SUPABASE_PROJECT_ID')

AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')

AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')

AWS_STORAGE_BUCKET_NAME = 'najot-talim-erp-bucket'

AWS_S3_ENDPOINT_URL = f'https://{SUPABASE_PROJECT_ID}.storage.supabase.co/storage/v1/s3'
AWS_S3_CUSTOM_DOMAIN = f'{SUPABASE_PROJECT_ID}.supabase.co/storage/v1/object/public/{AWS_STORAGE_BUCKET_NAME}'

AWS_DEFAULT_ACL = None
AWS_S3_FILE_OVERWRITE = True
AWS_QUERYSTRING_AUTH = False

AWS_S3_SIGNATURE_VERSION = 's3v4'

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
}
