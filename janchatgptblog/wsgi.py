"""
WSGI config for janchatgptblog project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os

try:
    from django.core.wsgi import get_wsgi_application
except ImportError:
    # Handle the import error
    print("Failed to import 'django.core.wsgi'. Ensure Django is installed.")
    get_wsgi_application = None

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'janchatgptblog.settings')

if get_wsgi_application:
    application = get_wsgi_application()
else:
    application = None
