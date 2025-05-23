"""
Django settings for src project.

Generated by 'django-admin startproject' using Django 5.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""



from pathlib import Path
import dj_database_url

from dotenv import load_dotenv
import os

load_dotenv() 
import cloudinary
import cloudinary.uploader
import cloudinary.api



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# ALLOWED_HOSTS = ['noahide.com', 'www.noahide.com']
ALLOWED_HOSTS = ['*']  # Allow all hosts for development purposes
  # Corrected name


# Application definition

DJANGO_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pwa'
]
PROJECT_APPS = ['accounts','blog','events','newsletter',]
THIRD_PARTY_APPS = [
    "sendgrid_backend",  # Email handling
    'ckeditor',
    
    "crispy_forms",
    "crispy_bootstrap5",
    'dbbackup',
    'django_crontab',
    'gunicorn',
    'cloudinary',
    'cloudinary_storage',
    'whitenoise',
   
   
   
    # "anymail",
   
]
INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTY_APPS

JAZZMIN_SETTINGS = {
    "site_title": "Noahide Wisdom",
    "site_header": "Noahide Wisdom Dashboard",
    "site_brand": "Rabbi Alexander",
    "welcome_sign": "Welcome to Noahide Wisdom",
    "show_ui_builder": True,  # Optional: Allows you to use a UI builder for the admin
     "site_url": "/",  # or your homepage path
}
JAZZMIN_UI_TWEAKS = {
    
    "theme": "flatly",
    "dark_mode_theme": "darkly",
    "sidebar": "nav-compact",
}



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
#done
ROOT_URLCONF = 'src.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["templates"],
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

WSGI_APPLICATION = 'src.wsgi.application'




DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': os.getenv('DATABASE_PORT'),
        'OPTIONS': {
            'sslmode': os.getenv('DATABASE_SSLMODE', 'require'),  # Default to 'require' if not set
        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators


# #filebased caching
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
#         'LOCATION': BASE_DIR / 'django_cache',  # Or any path on your filesystem
#     }
# }


#Memory caching 
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#     }
# }






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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/




CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # Corrected name
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

# WhiteNoise static files storage
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

    
#STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.CustomUser'




#Django DB Backup settings
DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': BASE_DIR / 'backup'}

# CRONJOBS = [
#     ('*/1 * * * *', 'config.perform_backup')  # every 1 minute projectname and function name
# ]
CRONJOBS = [
    ('*/1 * * * *', 'config.cron.perform_backup', '>> /tmp/db_backup.log 2>&1')
]


# Cloudinary Configuration from Environment Variables
CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.getenv("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": os.getenv("CLOUDINARY_API_KEY"),
    "API_SECRET": os.getenv("CLOUDINARY_API_SECRET"),
    
}

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
)






# Default message storage (session storage)
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# Customize message tags for Bootstrap compatibility

from django.contrib.messages import constants as message_constants

MESSAGE_TAGS = {
    message_constants.DEBUG: 'alert-info',
    message_constants.INFO: 'alert-info',
    message_constants.SUCCESS: 'alert-success',
    message_constants.WARNING: 'alert-warning',
    message_constants.ERROR: 'alert-danger',
}


# Disable email verification
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = "none"

# Redirect users after login/logout
  # Redirect to profile after login
  
# LOGIN_REDIRECT_URL = '/'
# LOGOUT_REDIRECT_URL = "signin"  # Redirect to login after logout

LOGIN_URL = 'signin'  # Your custom login URL name
LOGIN_REDIRECT_URL = '/'  # Where to go after login
LOGOUT_REDIRECT_URL = 'signin'  # Where to go after logout

#Upload path for ckeditor

CKEDITOR_UPLOAD_PATH = 'uploads/'

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': 700,
    }
}
#Email settings for AnymailResend

# EMAIL_BACKEND = "anymail.backends.resend.EmailBackend"
# ANYMAIL = {
#     "RESEND_API_KEY": os.getenv("RESEND_API_KEY", default=""),  # Provide a default
# }
# DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", default="no-reply@example.com")





# Email settings for SendGrid
EMAIL_BACKEND = 'sendgrid_backend.SendgridBackend'

SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')

# Optional: For debugging purposes in development
SENDGRID_SANDBOX_MODE_IN_DEBUG = False  # Set to True if you're testing without sending emails

# Optional: To track email status (useful for production)
SENDGRID_TRACK_EMAIL_OPENS = True

# Set default email address for sending
DEFAULT_FROM_EMAIL = "checheomenife@gmail.com"





# Import local settings if available
try:
    from .local_settings import *
except ImportError:
    print("No local settings found. Looks like you are in production.")