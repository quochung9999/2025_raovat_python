# Technical Context

This document describes the technical context. More details will be added as the project progresses.

## Database Credentials

PostgreSQL credentials depend on the machine ID. When working with PostgreSQL, especially in remote environments, always retrieve the current machine ID first to ensure the correct credentials are used.

### Machine ID: 2b04e5cc1d014b0897d12efeb29adb31

On this specific machine, the PostgreSQL server is configured to use **peer authentication** for local connections to the `postgres` database for the `postgres` system user.

This means that when connecting as the `postgres` operating system user to the `postgres` database on `localhost`, a database password is not required.

The command that successfully logs in using this method is:
`sudo -u postgres psql -d postgres`

If connecting from a different system user or using a different database, other authentication methods (like password authentication) may be required, and the appropriate credentials would be needed.

### Machine: aaa@aaa-Virtual-Machine (Machine ID Unknown)

For the machine identified as `aaa@aaa-Virtual-Machine`, the PostgreSQL credentials are:
- **Username:** `postgres`
- **Password:** `temp_password`

Note: The specific authentication method configured on this machine is not currently documented. You may need to use password authentication when connecting with these credentials.

## Web Server Configuration

The web application is deployed using a standard Django + Gunicorn + Nginx stack:

### Nginx

- **Version:** 1.18.0 (Ubuntu)
- **Configuration File:** `/etc/nginx/sites-available/raovat`
- **Enabled Site:** `/etc/nginx/sites-enabled/raovat` (symlink)
- **SSL Certificates:** Managed by Certbot at `/etc/letsencrypt/live/rauma24h.com/`
- **Domain Names:** `rauma24h.com`, `www.rauma24h.com`
- **IP Address:** `45.56.68.95`

### Gunicorn

- **Service File:** `/etc/systemd/system/gunicorn_raovat.service`
- **Workers:** 3
- **Binding:** Unix socket at `/var/www/2025_raovat_python/gunicorn.sock`
- **WSGI Application:** `classified_project.wsgi:application`

## Django Application

- **Version:** 5.1.7
- **Installation Path:** `/var/www/2025_raovat_python`
- **Virtual Environment:** `/var/www/2025_raovat_python/venv`
- **Main App:** `classified_project`
- **Main App Module:** `listings`

## API Framework

- **Framework:** Django REST Framework
- **Version:** 3.16.0
- **API URL Prefix:** `/api/`
- **ViewSets:**
  - `AdViewSet`: Manages ad resources
  - `CategoryViewSet`: Manages category resources
  - `SubCategoryViewSet`: Manages subcategory resources
- **Custom Permissions:**
  - `IsAuthorOrAdminOrModerator`: Allows authors, admins, and moderators to edit resources

## Database

- **Type:** PostgreSQL
- **Adapter:** psycopg2-binary

## Environment Detection and Credential Selection

To ensure the correct credentials and configurations are used, it is crucial to determine whether the environment is a live PC or a local development PC. This can be achieved by running the following Linux commands:

1.  **Check the hostname:**

    `hostname`

    This command will return the hostname of the machine. On a live PC, the hostname is likely to be a domain name or a server name. On a local development PC, the hostname is likely to be a more generic name.

2.  **Check the IP address:**

    `ip addr show`

    This command will return the IP addresses of the machine. On a live PC, the IP address is likely to be a public IP address. On a local development PC, the IP address is likely to be a private IP address (e.g., 192.168.x.x, 10.x.x.x).

3.  **Check for specific files or directories:**

    Check for the existence of files or directories that are specific to the live or local development environment. For example, you might check for the existence of a file containing the database credentials for the live environment.

Based on the environment detected, choose the appropriate credentials and configurations.
