# Progress

This document describes the project progress. More details will be added as the project progresses.

## Database Setup

Confirmed that the default PostgreSQL login using peer authentication for the `postgres` system user to the `postgres` database is working on this machine.

## API Implementation

- Implemented backend API using Django REST Framework with endpoints for ads, categories, and subcategories
- Created API test cases documentation in `api_test_cases.md`
- Fixed API endpoint issues:
  - Added missing import for `IsAuthorOrAdminOrModerator` permission class in `listings/api_views.py`
  - Resolved URL conflict between REST framework router-generated endpoints and custom API endpoint
  - Updated JavaScript code in the homepage template to use the new endpoint path
  - Installed Django REST Framework package in the virtual environment used by the Gunicorn service

## Server Configuration

- Documented the web application server configuration in `how_webapp_server_configed.md`
- Server is configured with Nginx as a reverse proxy to Gunicorn
- Gunicorn is configured as a systemd service to run the Django application
- SSL certificates are managed by Certbot
