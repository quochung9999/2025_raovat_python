# Active Context

This document describes the active context. More details will be added as the project progresses.

## Recent Activity

- Tested default PostgreSQL credentials on this machine. Confirmed that login as the `postgres` system user to the `postgres` database using peer authentication is successful and does not require a database password. Password-based login attempts were unsuccessful as the password was unknown.
- Implemented initial backend API using Django REST framework, including serializers, views, URL routing, and custom permissions for Ad management.
- Created comprehensive test case documentation for user functionalities (`user_test_cases.md`), admin functionalities (`admin_test_cases.md`), and API functionalities (`api_test_cases.md`) using Playwright MCP.
- Executed 10 core user test cases on the live website (`https://rauma24h.com`) using the Playwright MCP server. All executed tests passed.
- Fixed API endpoint issues:
  - Added missing import for `IsAuthorOrAdminOrModerator` permission class in `listings/api_views.py`
  - Resolved URL conflict between REST framework router-generated endpoints and custom API endpoint by moving the custom endpoint from `/api/subcategories/<int:category_id>/` to `/subcategories-by-category/<int:category_id>/`
  - Updated JavaScript code in the homepage template to use the new endpoint path
  - Installed Django REST Framework package in the virtual environment used by the Gunicorn service
- Created detailed documentation of the web application server configuration in `how_webapp_server_configed.md`
