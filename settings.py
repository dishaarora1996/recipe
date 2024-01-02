import os
from dotenv import load_dotenv


load_dotenv()


from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = True

ALLOWED_HOSTS = ["*"]



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    # 'rest_framework.authtoken',
    'drf_yasg',
    'admincontrol',
    'accounts',
    'attributemanage',
    'basic',
    'position',
    'brands',
    'businessgroup',
    "corsheaders",
    'category',
    'employee',
    'item',
    'languagemanage',
    'legalstatustype',
    'loan',
    'taxmanage',
    'unitofmeasure',
    'currency',
    'django_filters',
]

REST_FRAMEWORK={
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],

}
from datetime import timedelta
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': SECRET_KEY,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(days=1),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

CORS_ALLOW_ALL_ORIGINS=True
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "corsheaders.middleware.CorsMiddleware"
]

ROOT_URLCONF = 'casa_mazatlan.urls'

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

WSGI_APPLICATION = 'casa_mazatlan.wsgi.application'


#Mongo Db credentials

MONGO_DB_HOST = os.environ.get("MONGO_DB_HOST")
MONGO_DB_USER = os.environ.get("MONGO_DB_USER")
MONGO_DB_PASSWORD= os.environ.get("MONGO_DB_PASSWORD")
MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME")
MONGO_DB_PORT = os.environ.get("MONGO_DB_PORT")


DATABASES = {
    'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ.get("DB_NAME"),
            'USER': os.environ.get("DB_USER"),
            'PASSWORD': os.environ.get("DB_PASSWORD"),
            'HOST': os.environ.get("DB_HOST"),
            'PORT': os.environ.get("DB_PORT"),
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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True



STATIC_URL = 'static/'
if DEBUG:
    STATICFILES_DIRS = [BASE_DIR/'static']


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')
EMAIL_USE_TLS = True


# Logging Configuration
LOGGER_ROTATING_FILE_HANDLER_MESSAGES = 'logging.handlers.RotatingFileHandler'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        },
        'console': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'file_accounts': {
            'level': 'INFO',
            'class': LOGGER_ROTATING_FILE_HANDLER_MESSAGES,
            'filename': 'logs/accounts.log',
            'maxBytes': 1048576,  # 20 MB
            'backupCount': 2,
            'formatter': 'file',
            'delay': False
        },
        'file_admincontrol': {
            'level': 'INFO',
            'class': LOGGER_ROTATING_FILE_HANDLER_MESSAGES,
            'filename': 'logs/admincontrol.log',
            'maxBytes': 1048576,  # 20 MB = 20971520 Bytes
            'backupCount': 2,
            'formatter': 'file',
            'delay': False
        },
        'file_attributemanage': {
            'level': 'INFO',
            'class': LOGGER_ROTATING_FILE_HANDLER_MESSAGES,
            'filename': 'logs/attributemanage.log',
            'maxBytes': 1048576,  # 20 MB = 20971520 Bytes
            'backupCount': 2,
            'formatter': 'file',
            'delay': False
        },
        'file_basic': {
            'level': 'INFO',
            'class': LOGGER_ROTATING_FILE_HANDLER_MESSAGES,
            'filename': 'logs/basic.log',
            'maxBytes': 1048576,  # 20 MB = 20971520 Bytes
            'backupCount': 2,
            'formatter': 'file',
            'delay': False
        },
        'file_brands': {
            'level': 'INFO',
            'class': LOGGER_ROTATING_FILE_HANDLER_MESSAGES,
            'filename': 'logs/brands.log',
            'maxBytes': 1048576,  # 20 MB = 20971520 Bytes
            'backupCount': 2,
            'formatter': 'file',
            'delay': False
        },
        'file_businessgroup': {
            'level': 'INFO',
            'class': LOGGER_ROTATING_FILE_HANDLER_MESSAGES,
            'filename': 'logs/businessgroup.log',
            'maxBytes': 1048576,  # 20 MB = 20971520 Bytes
            'backupCount': 2,
            'formatter': 'file',
            'delay': False
        },
        'file_category': {
            'level': 'INFO',
            'class': LOGGER_ROTATING_FILE_HANDLER_MESSAGES,
            'filename': 'logs/category.log',
            'maxBytes': 1048576,  # 20 MB = 20971520 Bytes
            'backupCount': 2,
            'formatter': 'file',
            'delay': False
        },
        'file_currency': {
            'level': 'INFO',
            'class': LOGGER_ROTATING_FILE_HANDLER_MESSAGES,
            'filename': 'logs/currency.log',
            'maxBytes': 1048576,  # 20 MB = 20971520 Bytes
            'backupCount': 2,
            'formatter': 'file',
            'delay': False
        },
        'file_employee': {
            'level': 'INFO',
            'class': LOGGER_ROTATING_FILE_HANDLER_MESSAGES,
            'filename': 'logs/employee.log',
            'maxBytes': 1048576,  # 20 MB = 20971520 Bytes
            'backupCount': 2,
            'formatter': 'file',
            'delay': False
        },
        'file_globalsettings': {
            'level': 'INFO',
            'class': LOGGER_ROTATING_FILE_HANDLER_MESSAGES,
            'filename': 'logs/globalsettings.log',
            'maxBytes': 1048576,  # 20 MB = 20971520 Bytes
            'backupCount': 2,
            'formatter': 'file',
            'delay': False
        },
        'file_item': {
            'level': 'INFO',
            'class': LOGGER_ROTATING_FILE_HANDLER_MESSAGES,
            'filename': 'logs/item.log',
            'maxBytes': 1048576,  # 20 MB = 20971520 Bytes
            'backupCount': 2,
            'formatter': 'file',
            'delay': False
        },
        'file_languagemanage': {
            'level': 'INFO',
            'class': LOGGER_ROTATING_FILE_HANDLER_MESSAGES,
            'filename': 'logs/languagemanage.log',
            'maxBytes': 1048576,  # 20 MB = 20971520 Bytes
            'backupCount': 2,
            'formatter': 'file',
            'delay': False
        },
        'file_legalstatustype': {
            'level': 'INFO',
            'class': LOGGER_ROTATING_FILE_HANDLER_MESSAGES,
            'filename': 'logs/legalstatustype.log',
            'maxBytes': 1048576,  # 20 MB = 20971520 Bytes
            'backupCount': 2,
            'formatter': 'file',
            'delay': False
        },
        'file_loan': {
            'level': 'INFO',
            'class': LOGGER_ROTATING_FILE_HANDLER_MESSAGES,
            'filename': 'logs/loan.log',
            'maxBytes': 1048576,  # 20 MB = 20971520 Bytes
            'backupCount': 2,
            'formatter': 'file',
            'delay': False
        },
        'file_position': {
            'level': 'INFO',
            'class': LOGGER_ROTATING_FILE_HANDLER_MESSAGES,
            'filename': 'logs/position.log',
            'maxBytes': 1048576,  # 20 MB = 20971520 Bytes
            'backupCount': 2,
            'formatter': 'file',
            'delay': False
        },
        'file_taxmanage': {
            'level': 'INFO',
            'class': LOGGER_ROTATING_FILE_HANDLER_MESSAGES,
            'filename': 'logs/taxmanage.log',
            'maxBytes': 1048576,  # 20 MB = 20971520 Bytes
            'backupCount': 2,
            'formatter': 'file',
            'delay': False
        },
        'file_unitofmeasure': {
            'level': 'INFO',
            'class': LOGGER_ROTATING_FILE_HANDLER_MESSAGES,
            'filename': 'logs/unitofmeasure.log',
            'maxBytes': 1048576,  # 20 MB = 20971520 Bytes
            'backupCount': 2,
            'formatter': 'file',
            'delay': False
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        }
    },
    'loggers': {
        'django': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': True
        },
        'accounts': {
            'level': 'INFO',
            'handlers': ['file_accounts'],
            'propagate': True,
        },
        'admincontrol': {
            'level': 'INFO',
            'handlers': ['file_admincontrol'],
            'propagate': True,
        },
        'attributemanage': {
            'level': 'INFO',
            'handlers': ['file_attributemanage'],
            'propagate': True,
        },
        'basic': {
            'level': 'INFO',
            'handlers': ['file_basic'],
            'propagate': True,
        },
        'brands': {
            'level': 'INFO',
            'handlers': ['file_brands'],
            'propagate': True,
        },
        'businessgroup': {
            'level': 'INFO',
            'handlers': ['file_businessgroup'],
            'propagate': True,
        },
        'category': {
            'level': 'INFO',
            'handlers': ['file_category'],
            'propagate': True,
        },
        'currency': {
            'level': 'INFO',
            'handlers': ['file_currency'],
            'propagate': True,
        },
        'employee': {
            'level': 'INFO',
            'handlers': ['file_employee'],
            'propagate': True,
        },
        'globalsettings': {
            'level': 'INFO',
            'handlers': ['file_globalsettings'],
            'propagate': True,
        },
        'item': {
            'level': 'INFO',
            'handlers': ['file_item'],
            'propagate': True,
        },
        'languagemanage': {
            'level': 'INFO',
            'handlers': ['file_languagemanage'],
            'propagate': True,
        },
        'legalstatustype': {
            'level': 'INFO',
            'handlers': ['file_legalstatustype'],
            'propagate': True,
        },
        'loan': {
            'level': 'INFO',
            'handlers': ['file_loan'],
            'propagate': True,
        },
        'position': {
            'level': 'INFO',
            'handlers': ['file_position'],
            'propagate': True,
        },
        'taxmanage': {
            'level': 'INFO',
            'handlers': ['file_taxmanage'],
            'propagate': True,
        },
        'unitofmeasure': {
            'level': 'INFO',
            'handlers': ['file_unitofmeasure'],
            'propagate': True,
        }
    }
}



