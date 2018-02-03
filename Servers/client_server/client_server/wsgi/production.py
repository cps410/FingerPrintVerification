"""
NOT USED
"""

# """
# NOTE:
# This WSGI file should be linked on pythonanywhere in the file
# at /var/www/technocru_pythonanywhere_com_wsgi.py. This location
# is not where pythonanywhere looks so use the following command
# to link it to where it needs to go:
#
# ln -s techno_cru/wsgi.py /var/www/technocru_pythonanywhere_com_wsgi.py
#
# to get the project working as far as wsgi configuration goes.
# """
# # +++++++++++ DJANGO +++++++++++
# # To use your own Django app use code like this:
# import os
# import sys
#
# path = '/home/auth_server/sites/techno_cru'
# if path not in sys.path:
#     sys.path.append(path)
#
# os.environ['DJANGO_SETTINGS_MODULE'] = 'auth_server.settings'
#
# ## Uncomment the lines below depending on your Django version
# ###### then, for Django >=1.5:
# from django.core.wsgi import get_wsgi_application
# application = get_wsgi_application()
# ###### or, for older Django <=1.4
# #import django.core.handlers.wsgi
# #application = django.core.handlers.wsgi.WSGIHandler()
