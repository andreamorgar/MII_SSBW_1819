"""
WSGI config for proyecto project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

# import os
#
# from django.core.wsgi import get_wsgi_application
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto.settings')
#
# application = get_wsgi_application()



from django.conf import settings
from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.core.wsgi import get_wsgi_application
import os

# https://stackoverflow.com/questions/12800862/how-to-make-django-serve-static-files-with-gunicorn
# if settings.DEBUG:
#     application = StaticFilesHandler(get_wsgi_application())
# else:
#     application = get_wsgi_application()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto.settings')
application = StaticFilesHandler(get_wsgi_application())
