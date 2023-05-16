"""
WSGI config for settings project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')

application = get_wsgi_application()

# /usr/local/opt/nginx/nginx.conf
# include / usr / local / opt / nginx / conf.d / *.conf;
# include / usr / local / opt / nginx / sites - enabled / *;

# ln - s / opt / homebrew / etc / nginx / sites - available / default / opt / homebrew / etc / nginx / sites - enabled /

# ln -s /usr/local/opt/nginx/sites-available/default /usr/local/opt/nginx/sites-enabled/
#
# usr/local/etc/nginx/
#
# ln -s /usr/local/etc/nginx/sites-available/default /usr/local/etc/nginx/sites-enabled/
#
# include /usr/local/etc/nginx/conf.d/*.conf;
# include /usr/local/etc/nginx/sites-enabled/*;
# gunicorn --workers 4 --threads 4 settings.wsgi --timeout 30 --max-requests 10000 --log-level info
