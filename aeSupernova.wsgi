import sys
import os
import os.path

sys.path.append('/home/supernova/')
sys.path.append('/home/supernova/aeSupernova')
sys.path.append('/home/supernova/aeSupernova/aeSupernova')
sys.path.append('/home/supernova/public')
os.environ['DJANGO_SETTINGS_MODULE'] = 'aeSupernova.aeSupernova.settings'

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
