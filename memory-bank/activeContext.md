# Active Context

This document describes the active context. More details will be added as the project progresses.

## Recent Activity

- Tested default PostgreSQL credentials on this machine. Confirmed that login as the `postgres` system user to the `postgres` database using peer authentication is successful and does not require a database password. Password-based login attempts were unsuccessful as the password was unknown.
- Implemented initial backend API using Django REST framework, including serializers, views, URL routing, and custom permissions for Ad management.
- Created comprehensive test case documentation for user functionalities (`user_test_cases.md`) and admin functionalities (`admin_test_cases.md`) using Playwright MCP.
- Executed 10 core user test cases on the live website (`https://rauma24h.com`) using the Playwright MCP server. All executed tests passed.
