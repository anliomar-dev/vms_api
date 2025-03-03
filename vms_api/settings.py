"""
Django settings for vms_api project.

Generated by 'django-admin startproject' using Django 5.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
from decouple import config, Csv

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('DJANGO_SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())
HOST = config('HOST', cast=str)

if DEBUG:
    BASE_URL = "http://127.0.0.1:8000"
else:
    BASE_URL = f"https://{HOST}"

LOGIN_URL = '/vms/login/'
# Application definition
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'vms_app.apps.VmsAppConfig',
    'corsheaders',
    'rest_framework',
    'djoser',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'django_filters',
    'drf_spectacular',
    'drf_spectacular_sidecar',
]

MIDDLEWARE = [
    # 'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'vms_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'vms_api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('PORT'),
        'OPTIONS': {
            'client_encoding': 'UTF8',
        },
    }
}

# user model
AUTH_USER_MODEL = 'vms_app.User'


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Indian/Mauritius'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/statics/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'statics')
]
STATIC_ROOT = os.path.join(BASE_DIR, 'statics')


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# JWT SETUP
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SIMPLE_JWT = {
    'ROTATE_REFRESH_TOKENS': True,
    'ACCESS_TOKEN_LIFETIME': timedelta(days= config('ACCESS_TOKEN_LIFETIME', cast=int)),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=config('REFRESH_TOKEN_LIFETIME', cast=int)),
    'BLACKLIST_AFTER_ROTATION': True,
    "UPDATE_LAST_LOGIN": True,
}

# CORS SETUP
CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
)

CORS_ALLOW_HEADERS = (
    "accept",
    "authorization",
    "content-type",
    "user-agent",
    "x-csrftoken",
)

CORS_ALLOW_ALL_ORIGINS = False
# CORS_ALLOW_ORIGINS = []

# DJOSER SETUP
PASSWORD_RESET_CONFIRM_URL = 'vms/auth/reset_password/{uid}/{token}/'
DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': PASSWORD_RESET_CONFIRM_URL,
    'SEND_CONFIRMATION_EMAIL': False,
    'SEND_ACTIVATION_EMAIL': False,
    'PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND': True,
    'SERIALIZERS': {
        'user': 'vms_app.serializers.UserSerializer',
        'current_user': 'vms_app.serializers.CurrentUserSerializer',
        'user_create': 'vms_app.serializers.RegisterUserSerializer',
    }
}

PASSWORD_RESET_TIMEOUT = config('PASSWORD_RESET_TIMEOUT', cast=int)
if not DEBUG:
    SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', cast=int)
    SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', cast=bool)
    SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', cast=bool)
    CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', cast=bool)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = config('SECURE_HSTS_INCLUDE_SUBDOMAINS', cast=bool)
    SECURE_HSTS_PRELOAD = config('SECURE_HSTS_PRELOAD', cast=bool)

# DRF-SPECTACULAR SETUP
PROJECT_DESCRIPTION = """
    API for managing vouchers, including creation, generation, and status updates (paid, expired, redeemed). 
    Supports user management and voucher lifecycle handling. Built for efficient voucher tracking and updates
"""
SPECTACULAR_SETTINGS = {
    'TITLE': 'vms_api',
    'DESCRIPTION': PROJECT_DESCRIPTION,
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'REDOC_DIST': 'SIDECAR',
    'SWAGGER_UI_DIST': 'SIDECAR'
}

# EMAIL
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = config('EMAIL_BACKEND')
    EMAIL_HOST = config('EMAIL_HOST')
    EMAIL_PORT = config('EMAIL_PORT')
    EMAIL_USE_TLS = config('EMAIL_USE_TLS')
    EMAIL_HOST_USER = config('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
    DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')


# JAZZMIN
JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",
    "dark_mode_theme": "darkly",
}
JAZZMIN_SETTINGS = {
    "site_title": "MSUL",
    "site_header": "MSUL",
    "site_brand": "intermart",
    "site_logo": "images/logo.png",
    "welcome_sign": "Welcom to Msul VMS",
    "copyright": "msul",
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "icons": {
        "auth": "fas fa-user",
        "auth.Group": "fas fa-users-cog",
        "vms_app.user": "fas fa-users",
        "vms_app.Voucher": "fa-solid fa-file-invoice-dollar",
        "vms_app.VoucherRequest": "fas fa-file-signature",
        "vms_app.Client": "fas fa-user-tie",
        "vms_app.AuditTrail": "fas fa-calendar-check",
        "vms_app.Company": "fas fa-building",
        "vms_app.Shop": "fas fa-store",
        "token_blacklist.OutstandingToken": "fas fa-hourglass-half",
        "token_blacklist.BlacklistedToken": "fas fa-ban",
    },
    "topmenu_links": [
        {"name": "Swigger-ui doc",  "url": "/vms/api/schema/swagger-ui/"},
        {"name": "Redoc",  "url": "/vms/api/schema/redoc/"},
    ],
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": False,
    'custom_css': 'css/jazzmin_custom.css',
    "custom_js": None,
    "use_google_fonts_cdn": True,
    "show_ui_builder": True,

    "login_logo": "",
    "login_logo_dark": "",
    "login_logo_width": "200px",
    "login_title": "Welcome",
    "login_show_sidebar": False,
    "login_footer_text": "msul",
}