# cd ..//copy-fblog/blog-c
# docker-compose exec django-web python manage.py migrate 
# if starting new container

"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import environ, os
from pathlib import Path
import mimetypes
mimetypes.add_type("text/css", ".css", True)
# env for postgresql from .env django-environ
env = environ.Env()
environ.Env.read_env()
# Your secret key
SECRET_KEY = env("SECRET_KEY")
TWITTER_CLIENT_ID=env('TWITTER_0AUTH2_CLIENT_ID')
TWITTER_SECRET=env('TWITTER_OAUTH2_CLIENT_SECRET')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-t_w75oo*#78o%8st_z*z!9cc-wlwm=m%v$4-n*@a)hv6pn)tn@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# while empty with ALLOWED_HOSTS= [] normally, we fill it when using docker
# ALLOWED_HOSTS = env("DJANGO_ALLOWED_HOSTS","127.0.0.1").split(",")
# this is throwing error, lets hardcode teh allowed host
# testserver for testing
# django-app-bqqp3.ondigitalocean.app is the DO domain name
ALLOWED_HOSTS = [env("DJANGO_ALLOWED_HOSTS"), '127.0.0.1', 'testserver', 'localhost', 'blog-c.com', 'django-app-bqqp3.ondigitalocean.app']
# split used because we can set more than one host in the env and they will be split into a list


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',

    # static setting for deployment on DO 
    'whitenoise.runserver_nostatic', 
    'django.contrib.staticfiles',
    'blogapp',
    'mptt',
    'bootstrap5',
    'django_ckeditor_5',
    
    # django all auth

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    # 'allauth.socialaccount.providers.twitter',
    'allauth.socialaccount.providers.twitter_oauth2',  
    # all auth end
    'widget_tweaks',

    # for https
    'django_extensions',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # django all auth
    'allauth.account.middleware.AccountMiddleware',
    # django all auth end

    # FOR DEPLoyment
     'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

# BASE_DIR / 'templates'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'static'],
        # 'DIRS':[os.path.join(BASE_DIR, 'blogapp', 'account')], #added to test the DIRS settings for allauth
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

WSGI_APPLICATION = 'mysite.wsgi.application'

# settings for https
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True



# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases


# WE WILL CHANGE THE FORMER VALUES TO USE SUPABASE
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': env("DB_NAME"),
#         'USER': env("DB_USER"),
#         'PASSWORD': env("DB_PASSWORD"),
#         'HOST': env("DB_HOST"),
#         'PORT': env("DB_PORT"),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env("DATABASE_RENDER_NAME"),
        'USER': env("DATABASE_RENDER_USER"),
        'PASSWORD': env("DATABASE_RENDER_PASSWORD"),
        'HOST': env("DATABASE_RENDER_HOST"),
        'PORT': env("DATABASE_RENDER_PORT"),
    }
}


# django all auth
SOCIALACCOUNT_ADAPTER ='blogapp.adapter.CustomSocialAccountAdapter'
AUTHENTICATION_BACKENDS = (
    'allauth.account.auth_backends.AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# all auth account adapter configuration
ACCOUNT_EMAIL_REQUIRED = True  #sign in
ACCOUNT_USERNAME_REQUIRED = True   #sign in
ACCOUNT_AUTHENTICATION_METHOD = "email"  #this is for login
# ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'    #this is for login
ACCOUNT_EMAIL_VERIFICATION = 'optional'
LOGIN_REDIRECT_URL = '/'
ACCOUNT_UNIQUE_EMAIL=True
ACCOUNT_FORMS = {'signup': 'blogapp.form.MyCustomSignupForm'}

SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT=True #i guess i want the social account for which the email matched, is automatically added to the list of social accounts connected to the local account

# checking email for twitter and whether it will work without an email as  X oauth2 dont retunr email
SOCIALACCOUNT_EMAIL_REQUIRED =False

# needed this to be set to true. 
SOCIALACCOUNT_STORE_TOKENS =True
# ACCOUNT_USER_MODEL_USERNAME_FIELD=None #i guess it means to not require a username for log in?
# i forgot i already set this field. commenting it all out
# end auth

# email backend
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# # email settings
# EMAIL_HOST = 'smtp.gmail.com'  # Replace with your SMTP host
# EMAIL_HOST_USER = "rajkumarmech95@gmail.com"  # Your email address
# EMAIL_HOST_PASSWORD = "bkjh tzln ihue qzum"  # Your email password it was created in
# # https://myaccount.google.com/signinoptions/twosv?pli=1&rapt=AEjHL4Nh-lgeWD8yNpHIUCVGG50MG9g4FHX2gdEAk4REFZLKxmFtpXxz4i7RWR6ib1tXOrmAgf7JB1UUTZ9iHphrdX_bzHlhUtww_VQ9uOu_au1lf7Q2bQE

# EMAIL_PORT = 465  # SMTP port
# EMAIL_USE_SSL = True  # Use SSL for secure connection

# comment emailbackend and email settings for sendgrid

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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
# adding this to try resolve the issue of images not loading in page
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# for production
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = "blogapp.Myuser"


LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

MEDIA_URL = '/media/'
MEDIA_ROOT =  os.path.join(BASE_DIR, 'media')



# CK_EDITOR_5_UPLOAD_FILE_VIEW_NAME = "custom_upload_file"

customColorPalette = [
        {
            'color': 'hsl(4, 90%, 58%)',
            'label': 'Red'
        },
        {
            'color': 'hsl(340, 82%, 52%)',
            'label': 'Pink'
        },
        {
            'color': 'hsl(291, 64%, 42%)',
            'label': 'Purple'
        },
        {
            'color': 'hsl(262, 52%, 47%)',
            'label': 'Deep Purple'
        },
        {
            'color': 'hsl(231, 48%, 48%)',
            'label': 'Indigo'
        },
        {
            'color': 'hsl(207, 90%, 54%)',
            'label': 'Blue'
        },
    ]

CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': ['heading', '|', 'bold', 'italic', 'link',
                    'bulletedList', 'numberedList', 'blockQuote', 'imageUpload', ],

    },
    'extends': {
        'blockToolbar': [
            'paragraph', 'heading1', 'heading2', 'heading3',
            '|',
            'bulletedList', 'numberedList',
            '|',
            'blockQuote',
        ],
        'toolbar': ['heading', '|', 'outdent', 'indent', '|', 'bold', 'italic', 'link', 'underline', 'strikethrough',
        'code','subscript', 'superscript', 'highlight', '|', 'codeBlock', 'sourceEditing', 'insertImage',
                    'bulletedList', 'numberedList', 'todoList', '|',  'blockQuote', 'imageUpload', '|',
                    'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor', 'mediaEmbed', 'removeFormat',
                    'insertTable',],
        'image': {
            'toolbar': ['imageTextAlternative', '|', 'imageStyle:alignLeft',
                        'imageStyle:alignRight', 'imageStyle:alignCenter', 'imageStyle:side',  '|'],
            'styles': [
                'full',
                'side',
                'alignLeft',
                'alignRight',
                'alignCenter',
            ]

        },
        'table': {
            'contentToolbar': [ 'tableColumn', 'tableRow', 'mergeTableCells',
            'tableProperties', 'tableCellProperties' ],
            'tableProperties': {
                'borderColors': customColorPalette,
                'backgroundColors': customColorPalette
            },
            'tableCellProperties': {
                'borderColors': customColorPalette,
                'backgroundColors': customColorPalette
            }
        },
        'heading' : {
            'options': [
                { 'model': 'paragraph', 'title': 'Paragraph', 'class': 'ck-heading_paragraph' },
                { 'model': 'heading1', 'view': 'h1', 'title': 'Heading 1', 'class': 'ck-heading_heading1' },
                { 'model': 'heading2', 'view': 'h2', 'title': 'Heading 2', 'class': 'ck-heading_heading2' },
                { 'model': 'heading3', 'view': 'h3', 'title': 'Heading 3', 'class': 'ck-heading_heading3' }
            ]
        }
    },
    'list': {
        'properties': {
            'styles': 'true',
            'startIndex': 'true',
            'reversed': 'true',
        }
    }
}

CKEDITOR_5_FILE_UPLOAD_PERMISSION = "authenticated"
CKEDITOR_5_FILE_STORAGE = "blogapp.storage.CustomStorage"

# django all auth

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': env("GOOGLE_CLIENT_ID"),
            'secret': env("GOOGLE_CLIENT_SECRET"),
            'key': ''
        },
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'EMAIL_AUTHENTICATION': True,
        'VERIFIED_EMAIL':True,
    },
    'twitter_oauth2': {
        'APP': {
            'client_id': TWITTER_CLIENT_ID,
            'secret': TWITTER_SECRET,
        }, 
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        # https://github.com/pennersr/django-allauth/blob/main/allauth/socialaccount/providers/twitter_oauth2/provider.py
        'SCOPE': [
            "users.read",
            "tweet.read",
            'tweet.write',
        ],
        
        'EMAIL_AUTHENTICATION': True,
        'VERIFIED_EMAIL':True,
    },
     "twitter": {  # Use OAuth 1.0a instead of twitter_oauth2
        "APP": {
            "client_id": "your-api-key",  # API Key (not client_id)
            "secret": "your-api-secret",  # API Secret (not client_secret)
        },
        "SCOPE": ["email"],  # OAuth 1.0a supports email
    }
    

}

# django all auth

# celeery configuration
# settings.py

# Celery configuration
# CELERY_BROKER_URL = 'redis://redis/0'  # Using the Redis container running on your local machine

# now we will use the render rediss
CELERY_BROKER_URL = env('REDISS_URL') + '/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_BACKEND = 'redis://redis/0'  # Optional: store results in Redis
# btw the redult baclend shuld have a different database
# the caching is /1
# celery result backend was the cause of the restarts
# CELERY_RESULT_BACKEND = env('REDISS_URL') + '/2'
BROKER_CONNECTION_RETRY_ON_STARTUP = True





# OK SO all the sendgrid settings just f- vanished. wth
SENDGRID_API_KEY = env("SENDGRID_API_KEY")
EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
SENDGRID_SANDBOX_MODE_IN_DEBUG = False #false if we want to send emails in debug mode
SENDGRID_ECHO_TO_STDOUT=True


# also only verified emails work? add these, otherwise error. the default im providing the email i verified in sendgrid.
# also good idea to send the default email to env

# https://stackoverflow.com/questions/607819/django-email
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-from-email


#Default: 'webmaster@localhost'
# Default email address for automated correspondence from the site manager(s). This address is used 
# in the From: header of outgoing emails and can take any format valid in the chosen email sending protocol 
# we can try set it to anything
DEFAULT_FROM_EMAIL = "rajkumarmech95@gmail.com"
SERVER_EMAIL = DEFAULT_FROM_EMAIL
# https://docs.djangoproject.com/en/5.1/ref/settings/#server-email
# The email address that error messages come from, such as those sent to ADMINS and MANAGERS. This address is used in the 
# From: header and can take any format valid in the chosen email sending protocol.

# some logging configuration,
# https://docs.djangoproject.com/en/5.1/topics/logging/
# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "formatters": {
#         "verbose": {
#             "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
#             "style": "{",
#         },
#         "simple": {
#             "format": "{levelname} {message}",
#             "style": "{",
#         },
#     },
#     "filters": {
#         "require_debug_true": {
#             "()": "django.utils.log.RequireDebugTrue",
#         },
#     },
#     # If you’re testing, you may want to set the console handler to DEBUG to 
#     # see everything logged during development.
#     "handlers": {
#         "console": {
#             "level": "INFO",
#             "filters": ["require_debug_true"],
#             "class": "logging.StreamHandler",
#             "formatter": "simple",
#         },
#         "mail_admins": {
#             "level": "ERROR",
#             "class": "django.utils.log.AdminEmailHandler",
#         },
#     },
#     "loggers": {
#         "django": {
#             "handlers": ["console"],
#             "propagate": True,
#         },
#         "django.request": {
#             "handlers": ["mail_admins"],
#             "level": "ERROR",
#             "propagate": False,
#         },
#         "blog-c.custom": {
#             "handlers": ["console", "mail_admins"],
#             "level": "INFO",
#             "filters": ["special"],
#         },
#     },
# }


# commented out because of error in DO app
# LOGGING = {
#     # ...
#     "version": 1,
#     "handlers": {
#         "file": {
#             "class": "logging.FileHandler",
#             "filename": os.path.join(BASE_DIR, "logfiles", "general.log"),
#         },
#          "console": {  # Optional: Also log to console for debugging
#             "level": "DEBUG",
#             "class": "logging.StreamHandler",
#             "formatter": "simple",
#         },
#     },
#     "formatters": {
#         "verbose": {
#             "format": "{name} {levelname} {asctime} {module} {process:d} {thread:d} {message}",
#             "style": "{",
#         },
#         "simple": {
#             "format": "{levelname} {message}",
#             "style": "{",
#         },
#     },
#     "loggers": {
#         "__main__": {  # For test logs
#             "handlers": ["file"],
#             "level": "DEBUG",
#             "propagate": False,
#         },
#         "django": {  # Ensure Django logs are captured
#             "handlers": ["file", "console"],  # Use both file & console
#             "level": "DEBUG",
#             "propagate": True,
#         },
#         "django.request": {  # Capture request errors
#             "handlers": ["file"],
#             "level": "DEBUG",
#             "propagate": False,
#         },
#     },
# }

# using redis 6379 as cache
# https://docs.djangoproject.com/en/5.1/topics/cache/
# https://medium.com/django-unleashed/caching-in-django-with-redis-a-step-by-step-guide-40e116cb4540
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        # "LOCATION": "redis://redis/1",
        # new redis
        "LOCATION": env("REDISS_URL") + '/1',
    }
}
# when both django and redis are containerized, the location for redis will be 
# "redis://redis/0", where redis is the name of the service
# if django is not contanerised aka outside of docker, it has to listen to redis at the location url like
# redis://[[username]:[password]]@localhost:6379/0
# "redis://127.0.0.1:6379/0",



# for nginx https
# 🔐 Security Settings
# the nginx was constantly redirecting us to another location so ssl was turned to false
SECURE_SSL_REDIRECT = False  # Redirect all HTTP to HTTPS we made it false
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")  # Trust Nginx proxy

SESSION_COOKIE_SECURE = True  # Secure cookies
CSRF_COOKIE_SECURE = True  # Secure CSRF cookie

# https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/#production
# probably leading to failed csrf verifications
CSRF_TRUSTED_ORIGINS = ["https://localhost","https://localhost:1337", "https://blog-c.com"]