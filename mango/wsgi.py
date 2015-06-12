
import sys,os


"""
WSGI config for main project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

if "/usr/local/django/mango" not in sys.path : 
	sys.path.insert(0,"/usr/local/django/mango")


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mango.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
