# Backend API Guide

This guide provides information on how to use the backend API for the classifieds project.

## Base URL

The base URL for the API is `/api/`. All endpoint paths are relative to this base URL.

## Authentication

Authentication is required for write operations (POST, PUT, PATCH, DELETE) on Ad endpoints. Read operations (GET) on all endpoints are publicly accessible.

**Note:** API authentication methods (e.g., Token Authentication, JWT) need to be configured in the project settings and implemented. This guide will be updated with specific authentication instructions once that is set up.

## Endpoints

### Ads

- **URL:** `/api/ads/`
- **Methods:**
    - `GET`: List all approved ads.
        - **Query Parameters:**
            - `author_id` (optional, requires authentication): Filter ads by author ID.
            - `status` (optional, requires authentication): Filter ads by status (pending, approved, denied).
    - `POST` (requires authentication): Create a new ad.
        - **Request Body:** JSON object matching the AdSerializer fields (excluding `category`, `subcategory`, `author`, `status` which are set automatically or read-only).
- **URL:** `/api/ads/{id}/`
- **Methods:**
    - `GET`: Retrieve details of a specific approved ad.
    - `PUT` (requires authentication, author/admin/moderator only): Update a specific ad.
        - **Request Body:** JSON object matching the AdSerializer fields.
    - `PATCH` (requires authentication, author/admin/moderator only): Partially update a specific ad.
        - **Request Body:** JSON object with fields to update.
    - `DELETE` (requires authentication, author/admin/moderator only): Delete a specific ad.

### Categories

- **URL:** `/api/categories/`
- **Methods:**
    - `GET`: List all categories.
- **URL:** `/api/categories/{id}/`
- **Methods:**
    - `GET`: Retrieve details of a specific category.

### SubCategories

- **URL:** `/api/subcategories/`
- **Methods:**
    - `GET`: List all subcategories.
- **URL:** `/api/subcategories/{id}/`
- **Methods:**
    - `GET`: Retrieve details of a specific subcategory.

## Examples

**Note:** Examples will be added once authentication is configured.
