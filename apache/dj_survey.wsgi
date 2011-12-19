#!/usr/bin python
import os, sys
from django.core.handlers import wsgi

#Calculate the path based on the location of the WSGI script.

project = os.path.dirname(os.path.realpath(__file__))
workspace=os.path.dirname(project)

sys.path.insert(0, workspace)
sys.path.insert(1,os.path.join(workspace,'proj'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'proj.settings'

application = wsgi.WSGIHandler()

