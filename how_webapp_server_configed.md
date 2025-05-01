# Web Application Server Configuration

This document outlines how the Django web application is configured and deployed on the server.

## Overview

The web application is deployed using a standard Django + Gunicorn + Nginx stack:

- **Django**: The web framework that handles the application logic
- **Gunicorn**: WSGI HTTP server that runs the Django application
- **Nginx**: Web server that acts as a reverse proxy to Gunicorn

## Server Architecture

```
Client Request → Nginx → Gunicorn → Django Application
```

1. Client makes a request to `https://rauma24h.com`
2. Nginx receives the request and forwards it to Gunicorn via a Unix socket
3. Gunicorn processes the request using the Django application
4. Django generates a response which is sent back through Gunicorn and Nginx to the client

## Nginx Configuration

Nginx is configured to serve the application at `rauma24h.com` and `www.rauma24h.com`. It handles SSL termination and forwards requests to Gunicorn.

**Configuration File**: `/etc/nginx/sites-available/raovat`

Key components:
- Listens on port 443 (HTTPS)
- SSL certificates managed by Certbot
- Redirects HTTP to HTTPS
- Serves static files directly from `/var/www/2025_raovat_python/staticfiles/`
- Forwards other requests to Gunicorn via Unix socket at `/var/www/2025_raovat_python/gunicorn.sock`

```nginx
server {
    server_name rauma24h.com www.rauma24h.com 45.56.68.95;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        alias /var/www/2025_raovat_python/staticfiles/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/2025_raovat_python/gunicorn.sock;
    }

    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/rauma24h.com/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/rauma24h.com/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot
}

server {
    if ($host = www.rauma24h.com) {
        return 301 https://$host$request_uri;
    } # managed by Certbot

    if ($host = rauma24h.com) {
        return 301 https://$host$request_uri;
    } # managed by Certbot

    listen 80;
    server_name rauma24h.com www.rauma24h.com 45.56.68.95;
    return 404; # managed by Certbot
}
```

## Gunicorn Configuration

Gunicorn is configured as a systemd service to run the Django application.

**Service File**: `/etc/systemd/system/gunicorn_raovat.service`

Key components:
- Runs as root user (not recommended for production, but used in this setup)
- Uses 3 worker processes
- Binds to Unix socket at `/var/www/2025_raovat_python/gunicorn.sock`
- Serves the Django application using the WSGI application defined in `classified_project.wsgi:application`

```ini
[Unit]
Description=gunicorn daemon for raovat Django application
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/var/www/2025_raovat_python
ExecStart=/var/www/2025_raovat_python/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/var/www/2025_raovat_python/gunicorn.sock classified_project.wsgi:application

[Install]
WantedBy=multi-user.target
```

## Django Application

The Django application is installed at `/var/www/2025_raovat_python`. It uses a virtual environment located at `/var/www/2025_raovat_python/venv`.

Key components:
- Django 5.1.7
- Django REST Framework 3.16.0
- PostgreSQL database (using psycopg2-binary)

## API Configuration

The API is configured using Django REST Framework. The API endpoints are defined in `listings/api_urls.py` and included in the main `urls.py` file under the path `/api/`.

```python
# classified_project/urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/', include('listings.api_urls')),
    path('', include('listings.urls')),
]
```

```python
# listings/api_urls.py
router = DefaultRouter()
router.register(r'ads', api_views.AdViewSet)
router.register(r'categories', api_views.CategoryViewSet)
router.register(r'subcategories', api_views.SubCategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
```

There's also a custom API endpoint for getting subcategories by category ID, which is defined in `listings/urls.py`:

```python
# listings/urls.py
path('subcategories-by-category/<int:category_id>/', views.get_subcategories, name='api_get_subcategories'),
```

## Deployment Process

To deploy changes to the application:

1. Update the code in `/var/www/2025_raovat_python`
2. Restart the Gunicorn service:
   ```
   sudo systemctl restart gunicorn_raovat.service
   ```

## Troubleshooting

If the application is not working correctly, check the following:

1. Gunicorn service status:
   ```
   systemctl status gunicorn_raovat.service
   ```

2. Gunicorn logs:
   ```
   journalctl -u gunicorn_raovat.service
   ```

3. Nginx logs:
   ```
   tail -f /var/log/nginx/access.log
   tail -f /var/log/nginx/error.log
   ```

4. Django application logs (if configured)

## Recent Issues and Fixes

1. **API Endpoint Conflict**: There was a conflict between the REST framework's router-generated endpoints and a custom API endpoint. This was fixed by moving the custom endpoint from `/api/subcategories/<int:category_id>/` to `/subcategories-by-category/<int:category_id>/` and updating the JavaScript code in the homepage template to use the new endpoint path.

2. **Missing Django REST Framework**: The Django REST Framework package was not installed in the virtual environment used by the Gunicorn service. This was fixed by installing the package using pip:
   ```
   /var/www/2025_raovat_python/venv/bin/pip install djangorestframework
   ```

3. **Missing Import in API Views**: The `IsAuthorOrAdminOrModerator` permission class was not imported in `listings/api_views.py`. This was fixed by adding the import:
   ```python
   from .api_permissions import IsAuthorOrAdminOrModerator
