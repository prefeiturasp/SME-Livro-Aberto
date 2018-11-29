from .base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}


MIGRATION_MODULES = {
    'from_to_handler': None,
    'budget_execution': None,
}
