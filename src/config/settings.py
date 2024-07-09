from datetime import timedelta
from pathlib import Path
from . import local_settings as local

def p(text, green=True):
    if green:
        print(f"\033[32m{text}\033[0m")
    else:
        print(f'\033[31m{text}\033[0m')

def print_local_var(locals):
    for var, value in locals.items():
        print(f'{var} = {value}') 
    print('-----------------------------')

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure--v2ki54-tod(@cxcft#cxf7m8hy1rv5b9!!@d_tvxkhhy!h3_&'
API_VERSION = 'v1'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SITE_URL = "http://127.0.0.1:8000"

ALLOWED_HOSTS = []


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'apps.api',
    
    'apps.user',
    'apps.book',
    'apps.word',
    
    'rest_framework',
    'corsheaders',
    'djoser',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
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
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': local.NAME,
        'USER': local.USER,
        'PASSWORD': local.PASSWORD,
        'PORT': local.PORT,
        # 'HOST': '192.168.1.43', not working
        'HOST': local.HOST,
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR.joinpath("static/")





DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# AUTH 

AUTH_USER_MODEL = 'user.User'
AUTHENTICATION_BACKENDS = ('apps.user.backends.EmailOrUsernameModelBackend',)
 

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication'
    ],
    
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 2
}
SIMPLE_JWT = {
    # кол-во дней для того
    # чтобы зайти без пароля
    "ACCESS_TOKEN_LIFETIME": timedelta(days=7),
    # после этого времени пароль обязателен
    "REFRESH_TOKEN_LIFETIME": timedelta(days=60),
    # при запросе на обновление токена, ЕСЛИ False, будет 
    # возвращен только новый access-токен 
    "ROTATE_REFRESH_TOKENS": True,
    # будет ли refresh-токен добавлен в черный список после его обновления
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,

    'AUTH_HEADER_TYPES': ('JWT', 'Beare', 'Bearer'),

    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}



DJOSER = {
    # PASSWORD_RESET
    'USER_CREATE_PASSWORD_RETYPE': True,
    'SET_PASSWORD_RETYPE': True,
    'PASSWORD_RESET_CONFIRM_RETYPE': True,
    
    
    # вернет неверный ответ на запрос HTTP 400, если адрес электронной почты, 
    # указанный для запроса на сброс пароля, не существует в базе данных
    'PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND': True,
    'PASSWORD_RESET_CONFIRM_URL': '#/password/reset/confirm/{uid}/{token}',
    
    # EMAIL
    'SEND_ACTIVATION_EMAIL': True,
    'ACTIVATION_URL': 'api/users/activation/{uid}/{token}', # так будет выглядить url в писме на почту
    
    'TOKEN_MODEL': None, # we use only JWT 
    'SERIALIZERS': {
        'activation':  f'apps.api.{API_VERSION}.user.serializers.CustomActivationSerializer',
        'user_create_password_retype': f'apps.api.{API_VERSION}.user.serializers.CustomUserCreatePasswordRetypeSerializer',
        },
}

# EMAIL
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'django-backend@yandex.ru'
EMAIL_HOST_PASSWORD = 'yumetfpebogtnbpk'
EMAIL_USE_SSL = True

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# BOOK

PAGE_SIZE = 2000
PENALTY_SIZE = 100


# CORS

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3080",
    "http://localhost:5173",
]