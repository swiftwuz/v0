"""
WSGI config for v0 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from dotenv import load_dotenv
from django.core.wsgi import get_wsgi_application
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'v0.settings')

project_folder = os.path.expanduser(settings.BASE_DIR)  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env'))

application = get_wsgi_application()
