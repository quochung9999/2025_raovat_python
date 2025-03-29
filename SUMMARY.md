# Project Summary: Classified Ads Web Application

This project is a web application built using the **Django** framework and an **SQLite** database. It serves as a platform for users to post and browse classified advertisements.

## Core Functionality

1.  **User Authentication:** Standard registration (`signup`), login, and logout functionality using Django's built-in authentication system (`django.contrib.auth`). Uses a custom form (`CustomUserCreationForm`) for signup.
2.  **Ad Listings & Browsing:**
    *   A public homepage (`HomePageView`) displays a paginated list of all **approved** advertisements, ordered by creation date (newest first).
    *   Each approved ad has a dedicated detail page (`AdDetailView`) showing its full information.
3.  **User Ad Management (Logged-in Users):**
    *   Users can create new ads (`CreateAdView`). Submitted ads are initially set to **pending** status.
    *   A personal dashboard (`UserDashboardView`) allows users to see their own ads and their status (pending, approved, denied).
    *   Users can edit (`UpdateAdView`) their existing ads (resets status to **pending**).
    *   Users can delete (`DeleteAdView`) their own ads.
4.  **Admin Management Dashboard (Superusers Only):**
    *   A restricted section (`/manage/`) accessible only to superusers.
    *   **Category & Subcategory Management:** Full CRUD capabilities.
    *   **Ad Management (`AdminAdListView`):** View all ads, filter by status, bulk approve/deny.
    *   **User Management (`UserManagementListView`):** View users, ban/unban (cannot ban self/other superusers).
5.  **Dynamic Form Behavior:**
    *   An API endpoint (`/api/subcategories/<category_id>/`) fetches subcategories based on a selected category for dynamic form updates.

## Technical Logic & Structure

*   **Models (`listings/models.py`):** Defines `Category`, `SubCategory`, `Ad`.
*   **Views (`listings/views.py`):** Uses Django's class-based views for request handling and logic. Access control via mixins.
*   **URLs (`listings/urls.py`, `classified_project/urls.py`):** Maps URL paths to views. Includes Django auth URLs.
*   **Forms (`listings/forms.py`):** Defines forms for data input/validation.
*   **Templates (`templates/`):** HTML files using Bootstrap 5 for presentation.
*   **Settings (`classified_project/settings.py`):** Configures the Django project (apps, DB, static files, etc.).

## Analysis Process Diagram

```mermaid
graph TD
    A[User Request: Summarize Project] --> B{Analyze PLAN.md};
    B --> C{Analyze listings/models.py};
    C --> D{Analyze listings/views.py};
    D --> E{Analyze listings/urls.py};
    E --> F{Analyze classified_project/urls.py};
    F --> G[Synthesize Information];
    G --> H[Present Summary];