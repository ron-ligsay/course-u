from pathlib import Path
import os

from logging.handlers import RotatingFileHandler

from colorlog import ColoredFormatter

#from decouple import Config, RepositoryEnv
#config = Config(RepositoryEnv('.env'))
# config.read('.env')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-h_s31sn!wtc)#5sf1^c%*nvy)dp3t*5ja)n+g6*(0nw-wge(s='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
                #[]
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    #'django_light',
    #'admin_tools_stats',
    #'django_nvd3',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'management_commands',
    'apps.acad',
    'apps.assessment',
    'apps.recommender',
    'apps.jobs',
    'apps.personality',
    'apps.website',
    'grades',
    'apps.survey',
    'apps.recommender_survey',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'course_u.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR  / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                #'website.context_processors.context_question_sets',
            ],
        },
    },
]

INTERNAL_IPS= [
    '127.0.0.1',
]

WSGI_APPLICATION = 'course_u.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'courseu_db',
        'USER': 'root',
        'PASSWORD': '022002',#'sql2023',sawadeeKA456', #'022002'
        'HOST': 'localhost',
        'PORT': '3306',
    }
} 


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/


STATIC_URL = 'static/'
STATICFILES_DIRS = os.path.join(BASE_DIR, 'static'),
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')

MEDIA_URL = "images/" # STATIC AND MEDIA SHOULD HAVE DIFFERENT VALUES
MEDIA_ROOT = BASE_DIR/'static'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# typically, os.path.join(os.path.firname(__file__), 'media')))
# MEDIA_ROOT = 'website/templates/images'
# MEDIA_URL = '/images/'

#DISABLE_EXISITING_LOGGERS = False

LOGOUT_REDIRECT_URL = 'logout_success'


# Custom log Colors
log_colors = {
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
            }

FORMATTERS = ({
        "default" : {
            #"[{asctime}] {levelname} [{name}:{lineno}] {message}"
            "format" : "{levelname} {asctime:s} {name} {module} {filename} {lineno:d} {funcName} {message}",
            "style" : "{",
        },
        "verbose" : {
            "format" : "{levelname} {asctime:s} {name} {threadName} {thread:d} {module} {filename} {lineno:d} {name} {funcName} {process:d} {message}", 
            "style" : "{",
        },
        "simple" : {
            "format" : "{levelname} {asctime:s} {name} {module} {filename} {lineno:d} {funcName} {message}",
            "style" : "{",
        },
        "customize_1" : {
            "format" : "\033[1;32m{levelname} {message} ",
            "style" : "{",
        },
        "customize_2" : {
            "()": ColoredFormatter,
            "format": "%(log_color)s%(levelname)-8s%(reset)s %(message)s",
            "log_colors": log_colors,
        },
    })  


# Level of Debugs
# DEBUG - Detailed information, typically of interest only when diagnosing problems.
# INFO - Confirmation that things are working as expected.
# WARNING - An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). The software is still working as expected.
# ERROR - Due to a more serious problem, the software has not been able to perform some function.
# CRITICAL - A serious error, indicating that the program itself may be unable to continue running.


HANDLERS = {
    "console_handler": {
        "class" : "logging.StreamHandler",
        "formatter": "customize_2", # simple or verbose
        "level" :  "DEBUG"
    },
    "critical_handler": {
        "class":"logging.handlers.RotatingFileHandler",
        "filename":f"{BASE_DIR}/src/logs/critical.log",
        "mode":"a",
        "formatter":"verbose", #verbose
        "level" : "CRITICAL", # filter to only log messages with a level of WARNING or higher
        "backupCount":5,
        "maxBytes" : 1024 * 1024 * 5, # 5 MB
    },
    "warning_handler": {
        "class":"logging.handlers.RotatingFileHandler",
        "filename":f"{BASE_DIR}/src/logs/warning.log",
        "mode":"a",
        "formatter":"verbose", #verbose
        "level" : "WARNING", # filter to only log messages with a level of WARNING or higher
        "backupCount":5,
        "maxBytes" : 1024 * 1024 * 5, # 5 MB
    },
    "info_handler": {
        "class": "logging.handlers.RotatingFileHandler",
        "filename":f"{BASE_DIR}/src/logs/info.log",
        "mode":"a",
        "encoding":"utf-8",
        "formatter":"simple",
        "level":"INFO", # Filter out all messages with a level less than INFO
        "backupCount":5,
        "maxBytes":1024 * 1024 * 5 , # 5 MB
    },
    "error_handler": {
        "class":"logging.handlers.RotatingFileHandler",
        "filename":f"{BASE_DIR}/src/logs/error.log",
        "mode":"a",
        "formatter":"verbose", #verbose
        "level" : "WARNING", # filter to only log messages with a level of WARNING or higher
        "backupCount":5,
        "maxBytes" : 1024 * 1024 * 5, # 5 MB
    },
}

LOGGERS = (
    {
        "django" : { # name of the logger
        "handlers" : ["console_handler","info_handler"],
            "level" : 'INFO',
        },
        "django.request" : {
            "handlers" : ["error_handler"],
            "level" : "INFO",
            "propagate" : True,
        },
        "dango.template" : {
            "handlers" : ["error_handler"],
            "level" : "INFO",
            "propagate" : True,
        },
        "django.server" : {
            "handlers" : ["error_handler"],
            "level" : "INFO",
            "propagate" : True,
        },
    },
)

LOGGING = {
    "version" : 1,
    "disable_existing_loggers" : False,
    "formatters" : FORMATTERS,#
    "handlers" : HANDLERS, 
    "loggers" : LOGGERS[0], #[0] name of the logger
    # "incremental" : True,
    # "filters" : {},
}

# LOGGING_CONFIG = None

# import logging.config

# logging.config.dictConfig(LOGGING)

JAZZMIN_SETTINGS = {
    #for admin page
    "show_ui_builder": False,
    'site_header': "Course-U",
    'site_brand': "Course-U",
    'site_logo': "images/logo.png",
    "site_icon": "images/logo.png",
    'copyright': "courseu-production-d2b3.up.railway.app",
    "search_model": ["auth.User", "auth.Group"],
    "navigation_expanded": False,
    "changeform_format": "collapsible",
    #"default_icon_parents": "fas fa-chevron-circle-right",
    #"default_icon_children": "fas fa-circle",
    "icons": {
    "auth": "fas fa-users-cog",
    "auth.user": "fas fa-user",
    "users.User": "fas fa-user",
    "auth.Group": "fas fa-users",
    "admin.LogEntry": "fas fa-file",
    },

    #for admin login
    'login_logo': "images/boy.png",
    "welcome_sign": "Welcome to the Course-U Administrator",
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-orange",
    "accent": "accent-orange",
    "navbar": "navbar-orange navbar-light",
    "no_navbar_border": True,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-light-orange",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "minty",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
    "actions_sticky_top": True
}

