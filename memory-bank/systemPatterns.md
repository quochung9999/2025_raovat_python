# System Patterns

This document describes the system patterns. More details will be added as the project progresses.

## Server Architecture

The web application follows a standard Django + Gunicorn + Nginx stack architecture:

```
Client Request → Nginx → Gunicorn → Django Application
```

1. Client makes a request to `https://rauma24h.com`
2. Nginx receives the request and forwards it to Gunicorn via a Unix socket
3. Gunicorn processes the request using the Django application
4. Django generates a response which is sent back through Gunicorn and Nginx to the client

## API Design Patterns

The API follows RESTful design principles using Django REST Framework:

1. **Resource-Based URLs**: Resources are accessed through URLs that represent the resource type (e.g., `/api/ads/`, `/api/categories/`).

2. **HTTP Methods**: Standard HTTP methods are used for CRUD operations:
   - GET: Retrieve resources
   - POST: Create new resources
   - PUT/PATCH: Update existing resources
   - DELETE: Remove resources

3. **ViewSets and Routers**: Django REST Framework's ViewSets and Routers are used to automatically generate URL patterns for resources.

4. **Serializers**: Serializers are used to convert complex data types (like Django models) to and from Python native datatypes that can be rendered into JSON.

5. **Permission Classes**: Custom permission classes are used to control access to resources based on user roles and ownership.

## URL Patterns

1. **API Endpoints**: All API endpoints are prefixed with `/api/` and follow RESTful conventions.
   - `/api/ads/`: List all ads or create a new ad
   - `/api/ads/{id}/`: Retrieve, update, or delete a specific ad
   - `/api/categories/`: List all categories
   - `/api/categories/{id}/`: Retrieve a specific category
   - `/api/subcategories/`: List all subcategories
   - `/api/subcategories/{id}/`: Retrieve a specific subcategory

2. **Custom API Endpoints**: Custom API endpoints are used for specific functionality that doesn't fit the RESTful pattern.
   - `/subcategories-by-category/{category_id}/`: Get subcategories for a specific category

3. **Admin URLs**: Admin URLs are prefixed with `/manage/` and provide access to administrative functions.
   - `/manage/`: Admin dashboard
   - `/manage/ads/`: Manage ads
   - `/manage/users/`: Manage users
   - `/manage/flags/`: Manage user flags
   - `/manage/categories/`: Manage categories
   - `/manage/subcategories/`: Manage subcategories

4. **User URLs**: User-specific URLs provide access to user functions.
   - `/dashboard/`: User dashboard
   - `/dashboard/ad/{id}/edit/`: Edit a specific ad
   - `/dashboard/ad/{id}/delete/`: Delete a specific ad

5. **Authentication URLs**: Authentication URLs are prefixed with `/accounts/` and provide access to authentication functions.
   - `/accounts/login/`: Login
   - `/accounts/logout/`: Logout
   - `/signup/`: Sign up
