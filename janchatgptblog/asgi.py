"""
ASGI config for janchatgptblog project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

try:
    from django.core.asgi import get_asgi_application
except ImportError:
    raise ImportError("Failed to import 'django.core.asgi'. Ensure Django is installed.")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'janchatgptblog.settings')

application = get_asgi_application()
