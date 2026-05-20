from pathlib import Path
import environ
import os

env = environ.Env(
    DEBUG=(bool, False)
)

BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env('SECRET_KEY')


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
    'notifications',
    'teachers',
    'students',
    'staffs',

    #Third party applar
    'django_filters',
    'rest_framework',
    'storages',
    "debug_toolbar",
    'django_extensions',
]

INTERNAL_IPS = [
    "127.0.0.1",
]

MIDDLEWARE = [
    'django_request_cache.middleware.RequestCacheMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",
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
        'DIRS': [str(BASE_DIR.joinpath('templates'))],
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

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
        "CONN_HEALTH_CHECKS": True,
        'CONN_MAX_AGE': env.int('DB_CONN_MAX_AGE', default=300),
        'DISABLE_SERVER_SIDE_CURSORS': env.bool('DB_DISABLE_SERVER_SIDE_CURSORS', default=True),
        'OPTIONS': {
            'sslmode': env('DB_SSLMODE'),
            'connect_timeout': env.int('DB_CONNECT_TIMEOUT', default=5),
        },
    }
}

# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_TZ = True

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'student-dashboard'
LOGOUT_REDIRECT_URL = 'login'

AUTH_USER_MODEL = 'users.User'

USE_S3_STORAGE = env.bool('USE_S3_STORAGE', default=True)

STATICFILES_DIRS = [BASE_DIR / 'static']

if USE_S3_STORAGE:
    SUPABASE_PROJECT_ID = env('SUPABASE_PROJECT_ID')
    AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = env(
        'AWS_STORAGE_BUCKET_NAME',
        default='najot-talim-erp-bucket',
    )

    AWS_S3_ENDPOINT_URL = (
        f'https://{SUPABASE_PROJECT_ID}.storage.supabase.co/storage/v1/s3'
    )
    AWS_S3_CUSTOM_DOMAIN = (
        f'{SUPABASE_PROJECT_ID}.supabase.co/storage/v1/object/public/'
        f'{AWS_STORAGE_BUCKET_NAME}'
    )

    AWS_DEFAULT_ACL = None
    AWS_S3_FILE_OVERWRITE = True
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_SIGNATURE_VERSION = 's3v4'
    AWS_S3_ADDRESSING_STYLE = 'path'

    STORAGES = {
        'default': {
            'BACKEND': 'storages.backends.s3.S3Storage',
            'OPTIONS': {
                'location': 'media',
                'file_overwrite': True,
            },
        },
        'staticfiles': {
            'BACKEND': 'storages.backends.s3.S3StaticStorage',
            'OPTIONS': {
                'location': 'static',
            },
        },
    }

    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
else:
    STATIC_URL = '/static/'
    STATIC_ROOT = BASE_DIR / 'staticfiles'
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'