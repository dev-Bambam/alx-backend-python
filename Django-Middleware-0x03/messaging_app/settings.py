from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-3x#z#i2p@8_95t620&1!3p2@z)3z0e=f0^@w9*x81y=0-j1(p='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework', # Added DRF
    'chats', # Added the messaging app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # NEW: Restrict access must happen BEFORE authentication or any other logic
    'chats.middleware.RestrictAccessByTimeMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    
    # CRITICAL: Register your custom middleware here. 
    # Must be after AuthenticationMiddleware to access request.user.
    'chats.middleware.RequestLoggingMiddleware', 
    
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'messaging_app.urls'

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

WSGI_APPLICATION = 'messaging_app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- Custom User Model ---
AUTH_USER_MODEL = 'chats.User'

# --- Django REST Framework Settings ---
REST_FRAMEWORK = {
    # CRITICAL: Set JWT (Bearer Token) as the default method for authentication
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication', # Used for Browsable API
    ),
    # Set the default permission to only allow authenticated users access
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    # ADDED: Include filters for ViewSet checks
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.SearchFilter',
    )
}

# --- SIMPLE JWT Configuration ---
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60), # Access tokens are valid for 60 minutes
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),  # Refresh tokens are valid for 7 days
    'ROTATE_REFRESH_TOKENS': True, # Enhances security
    'AUTH_HEADER_TYPES': ('Bearer',), # Standard header type for API tokens
}

# --- Logging Configuration (NEW) ---
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            # This handler writes to the requests.log file at the project root
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'requests.log', 
        },
    },
    'loggers': {
        # Define a custom logger to capture our request info
        'request_logger': { 
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
