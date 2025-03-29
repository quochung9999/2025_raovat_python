# Project Summary: Classified Ads Web Application

This project is a web application built using the **Django** framework and an **SQLite** database. It serves as a platform for users to post and browse classified advertisements.

## Core Functionality

1.  **User Authentication:** Standard registration (`signup`), login, and logout functionality using Django's built-in authentication system (`django.contrib.auth`). Uses a custom form (`CustomUserCreationForm`) for signup.
2.  **Ad Listings & Browsing:**
    *   A public homepage (`HomePageView`) displays a paginated list of all **approved** advertisements, ordered by creation date (newest first).
    *   **Homepage Filtering:** Users can filter ads by keyword (title/description), category, and subcategory. Includes a "Reset" button.
    *   Each approved ad has a dedicated detail page (`AdDetailView`) showing its full information.
3.  **User Ad Management (Logged-in Users):**
    *   Users can create new ads (`CreateAdView`). Submitted ads are initially set to **pending** status.
    *   **Pricing Options:** When creating/editing ads, users can select a pricing type (Fixed Price, Per Hour, Negotiable, Free). The price field is shown/required only when relevant (Fixed, Per Hour).
    *   A personal dashboard (`UserDashboardView`) allows users to see their own ads and their status (pending, approved, denied).
    *   Users can edit (`UpdateAdView`) their existing ads (resets status to **pending**).
    *   Users can delete (`DeleteAdView`) their own ads.
4.  **Moderator Role & Actions:**
    *   A "Moderator" user group exists with specific permissions.
    *   Moderators can access the Ad Management list (`AdminAdListView`) to view, approve, or deny selected pending ads.
    *   Moderators can flag users from the Ad Detail page (`FlagUserView`), providing a reason (Spam, Scam, Hack, Other) and optional details.
5.  **Admin Management Dashboard (Superusers Only):**
    *   A restricted section (`/manage/`) accessible only to superusers (except Ad Management, accessible by Moderators too).
    *   **Mobile-Friendly UI:** Admin list views (Ads, Categories, Subcategories, Users, Flags) use a responsive layout (table on desktop, cards on mobile). Forms are styled for better mobile usability.
    *   **Category & Subcategory Management:** Full CRUD capabilities.
    *   **Ad Management (`AdminAdListView`):** View all ads, filter by status, bulk approve/deny selected or all pending ads.
    *   **User Management (`UserManagementListView`):** View users, ban/unban, assign/remove Moderator role. Cannot modify self or other superusers.
    *   **Flag Review (`FlaggedUserListView`):** View pending user flags submitted by moderators. Admins can ban selected flagged users or all users with pending flags. Flags are marked as resolved after review.
6.  **Dynamic Form Behavior:**
    *   An API endpoint (`/api/subcategories/<category_id>/`) fetches subcategories based on a selected category for dynamic updates in the Homepage filter and Ad form.
    *   Ad form dynamically shows/hides the price field based on the selected pricing type.

## Technical Logic & Structure

*   **Models (`listings/models.py`):** Defines `Category`, `SubCategory`, `Ad` (with `price_type`), and `UserFlag`.
*   **Views (`listings/views.py`):** Uses Django's class-based views. Access control via `LoginRequiredMixin`, `SuperuserRequiredMixin`, `UserPassesTestMixin`. Includes views for CRUD, listing, flagging, and flag review.
*   **URLs (`listings/urls.py`, `classified_project/urls.py`):** Maps URL paths to views. Includes Django auth URLs, API endpoint, moderator, and admin paths.
*   **Forms (`listings/forms.py`):** Defines forms (`AdForm`, `CategoryForm`, `SubCategoryForm`, `CustomUserCreationForm`, `UserFlagForm`) with validation logic (e.g., conditional price requirement).
*   **Templates (`templates/`):** HTML files using Bootstrap 5. Admin templates use responsive table/card layouts. Partials used for status badges and pagination. JavaScript handles dynamic subcategory loading and conditional field display.
*   **Middleware (`listings/middleware.py`):** `RoleMiddleware` adds `is_moderator` attribute to `request.user`.
*   **Settings (`classified_project/settings.py`):** Configures Django project, including `ALLOWED_HOSTS` and added `RoleMiddleware`.
*   **Admin (`listings/admin.py`):** Registers models (`Category`, `SubCategory`, `Ad`, `UserFlag`, `Group`) with the Django admin site.

## Setup Notes

*   Requires creation of a "Moderators" group in Django admin with specific permissions assigned (`listings | ad | Can change ad`, `listings | ad | Can view ad`, `listings | user flag | Can add user flag`, `listings | user flag | Can view user flag`).