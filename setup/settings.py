import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta
from django.contrib.messages import constants as messages

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv()


SECRET_KEY = os.environ.get("SECRET_KEY", "INSECURE")
DEBUG = True if os.environ.get("DEBUG") == '1' else False
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']


# Application definition
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #Project Apps
    'apps.customer.apps.CustomerConfig',
    'apps.store.apps.StoreConfig',
    'apps.userauths.apps.UserauthsConfig',
    'apps.vendor.apps.VendorConfig',


    'apps.api.apps.ApiConfig',
    'apps.ecommerce.apps.EcommerceConfig',

    #Libraries installed
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'debug_toolbar',
    'drf_yasg',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    ################ Libraries ############################
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    ######################################################
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'setup.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'setup.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DATABASE_ENGINE'),
        'NAME': os.environ.get('DATABASE_NAME'),
        'USER': os.environ.get('DATABASE_USER'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
        'HOST': os.environ.get('DATABASE_HOST'),
        'PORT':os.environ.get('DATABASE_PORT'),
        'OPTIONS': {
            'charset': os.environ.get('DATABASE_CHARSET'),
            'init_command': os.environ.get('DATABASE_INIT_COMMAND'),
        }
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



# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'pt-pt'
TIME_ZONE = 'Africa/Luanda'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

############################################### Extra Config ##############################################################
# Customized User model
AUTH_USER_MODEL = 'userauths.User'


CORS_ORIGIN_ALLOW_ALL = True
# CORS_ORIGIN_WHITELIST = (
#     'localhost:8000',
#     '127.0.0.1:9000'
# )

FRONTEND_SERVER_URL = os.environ.get("FRONTEND_SERVER_URL")

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'local_static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# Ficheiros acima de 2MB vão p/ a o TemporaryMemory, baixo p/ o InMemory
FILE_UPLOAD_MAX_MEMORY_SIZE=2000000

# configuração das mensages de alertas passados nos views
MESSAGE_TAGS ={
    messages.ERROR: 'danger',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
}


EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = bool(os.environ.get('EMAIL_USE_TLS', True))
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
EMAIL_HOST = os.environ.get('EMAIL_HOST', '')

# django toolbar
INTERNAL_IPS = [
    "127.0.0.1",
]


# https://django-jazzmin.readthedocs.io/


JAZZMIN_SETTINGS = {
    'site_title': "Necrus",
    'site_header':"Necrus",
    'site_brand':"Necrus",
    "site_logo": "assets/img/logo/logo.png",
    "login_logo": "assets/img/logo/logo.png",
    "site_icon": "assets/img/logo/logo.png",
    "welcome_sign": "Bem Vindo a Administração da Necrus",
    'copyright':"Necrus",
    'show_sidebar':True,
    'show_ui_builder':True,
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=50),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',

    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# CKEDITOR_UPLOAD_PATH = 'media-contents/'
# CKEDITOR_CONFIGS = {
#     'default':{
#         'skin': 'moono',
#         'codeSnippet_theme':'monokai',
#         'toolbar': 'all',
#         'extraPlugins' : ','.join(
#             [
#                 'codesnippet',
#                 'widget',
#                 'dialog'
#             ]
#         ),
#     }
# }

