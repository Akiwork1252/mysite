from .settings_common import * 


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-5-ik6*(^eek(s(z*nxj!l3f)ogf=(v86l^7k+wpge7wq89)bq#'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = []


# ロギング
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'task_manager': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },

    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'dev',
        },
    },

    'formatters': {
        'dev': {
            'format': '\t'.join([
                '%(asctime)s',
                '[%(levelname)s]',
                '%(pathname)s(Line:%(lineno)d)',
                '%(message)s',
            ])
        },
    }
}


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
