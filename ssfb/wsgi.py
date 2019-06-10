"""
WSGI config for ssfb project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
import dotenv
from django.core.wsgi import get_wsgi_application

dotenv.read_dotenv()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ssfb.settings')

application = get_wsgi_application()
