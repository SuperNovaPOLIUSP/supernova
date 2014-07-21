#########################
# settings.py
#
# This is a Django settings file with debug set to False, and any sensitive
# variables set to empty strings.
# It can be checked in to version control or made public without fear, since
# the critical variables are loaded from a different file.

TEMPLATE_DEBUG = DEBUG = False

DATABASE_ENGINE = ''
DATABASE_NAME = ''
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''
SECRET_KEY = ''

# Then load those sensitive settings from a local file with tight
# filesystem permissions.
from os.path import expanduser
execfile(expanduser('~/.django-settings.py'))
