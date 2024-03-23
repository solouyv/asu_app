"""
WSGI config for asu_app project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# app_path = os.path.abspath(os.path.join(
#     os.path.dirname(os.path.abspath(__file__)), os.pardir))
# sys.path.append(os.path.join(app_path, 'api'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'asu_app.settings')

application = get_wsgi_application()
