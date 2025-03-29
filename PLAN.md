# Classified Web Application Plan (Django + SQLite)

## Website Functionality Summary

This application provides a platform for users to post and browse classified advertisements. Key features include:

*   **User Authentication:** Secure user registration, login, and logout capabilities.
*   **Ad Listings:**
    *   Public homepage displaying all approved advertisements.
    *   Detailed view page for each individual ad.
*   **User Ad Management:**
    *   Registered users can create new advertisements (submitted for admin approval).
    *   A personal dashboard allows users to view the status (pending, approved, denied) of their ads.
    *   Users can edit or delete their own advertisements.
    *   The user's ad list is presented in a mobile-friendly card format.
*   **Admin Dashboard & Tools:**
    *   A restricted admin section for site management.
    *   Full CRUD (Create, Read, Update, Delete) management for ad Categories and Subcategories.
    *   Comprehensive ad management: View all ads, approve or deny pending ads (individually or in bulk).
    *   User management capabilities.
*   **Deployment Configuration:**
    *   Configured to be accessible over the network via `0.0.0.0:8000`.
    *   Firewall rules updated to allow traffic on port 8000.
    *   Domain `hung0604.tplinkdns.com` added to allowed hosts.

---

## Phase 1: Project Setup & Core Models

1.  **Initialize Django Project:**
    *   Create a new Django project named `classified_project`.
    *   Create a Django app within the project called `listings`.
    *   Configure `settings.py`:
        *   Add `listings` to `INSTALLED_APPS`.
        *   Confirm SQLite database configuration.
        *   Configure static files (`STATIC_URL`, `STATICFILES_DIRS`).
        *   Configure `TEMPLATES` directory.
2.  **Define Database Models (`listings/models.py`):**
    *   `Category`: `name`, `slug`, `description` (optional).
    *   `SubCategory`: `name`, `slug`, `description` (optional), `category` (ForeignKey).
    *   `Ad`: `title`, `description`, `price` (optional), `location` (optional), `category` (ForeignKey), `subcategory` (ForeignKey), `author` (ForeignKey to `User`), `status` ('pending', 'approved', 'denied'), `created_at`, `updated_at`, `image` (optional).
3.  **Database Migrations:**
    *   Run `python manage.py makemigrations listings`.
    *   Run `python manage.py migrate`.
4.  **Create Superuser (Admin):**
    *   Run `python manage.py createsuperuser` (user: `bbb`, pass: `bbb`).

## Phase 2: User Authentication & Basic Views

5.  **Setup Authentication URLs:**
    *   Include `django.contrib.auth.urls`.
6.  **Create Basic Templates:**
    *   `base.html` (Bootstrap 5, responsive).
    *   `registration/login.html`.
    *   `registration/signup.html`.
    *   `home.html`.
7.  **Create Basic Views (`listings/views.py`):**
    *   `HomePageView`.
    *   `SignUpView` (using `UserCreationForm`).
8.  **Configure URLs (`listings/urls.py`, main `urls.py`):**
    *   Map homepage, login, logout, signup.

## Phase 3: Ad Posting & Display

9.  **Ad Creation Form (`listings/forms.py`):**
    *   `ModelForm` for `Ad`.
10. **Ad Creation View (`listings/views.py`):**
    *   `CreateAdView` (`LoginRequiredMixin`), saves ad as 'pending'.
11. **Ad Detail View (`listings/views.py` & Template):**
    *   `AdDetailView` for approved ads.
    *   `ad_detail.html` template.
12. **Update Homepage View:**
    *   Show only 'approved' ads.
13. **User Dashboard:**
    *   `UserDashboardView` to show user's ads and status.
    *   `dashboard.html` template.
    *   `ad_list_table.html` partial template for the list.
14. **Update URLs:**
    *   Add URLs for ad creation, detail view, dashboard, ad update, ad delete.

## Phase 4: Admin Tools Page

15. **Admin Access Control:**
    *   Decorator/middleware to restrict admin views to superuser (`is_superuser`).
16. **Category/SubCategory Management (`listings/views.py`, `forms.py`, Templates):**
    *   CRUD views (ListView, CreateView, UpdateView, DeleteView) for `Category` & `SubCategory`.
    *   Forms (`CategoryForm`, `SubCategoryForm`).
    *   Admin-only templates.
17. **Ad Management View (`listings/views.py` & Template):**
    *   `AdminAdListView` (admin-only).
    *   Display ads with status, checkboxes for selection.
    *   Buttons: "Approve Selected", "Deny Selected", "Approve All Pending", "Deny All Pending".
    *   Implement bulk action logic (POST).
    *   `admin_ad_list.html` template.
18. **User Management View (`listings/views.py` & Template):**
    *   `UserManagementListView` (admin-only).
    *   Display users, potentially with options to manage roles/status.
    *   `user_management_list.html` template.
19. **"TOOLS" Page Structure:**
    *   `tools.html` (admin-only) linking to management sections.
20. **Update URLs:**
    *   Add admin URLs under `/tools/`.

## Phase 5: Refinement & Styling

21. **Bootstrap Integration:**
    *   Ensure templates use Bootstrap effectively for layout and responsiveness.
22. **Styling:**
    *   Add custom CSS as needed.
23. **Testing:**
    *   Manual testing of all features and responsiveness.

## Phase 6: Deployment & Mobile UI Enhancement

24. **Network Accessibility:**
    *   Opened port 8000 on the server firewall (`sudo ufw allow 8000/tcp`).
    *   Configured `ALLOWED_HOSTS` in `settings.py` to include `hung0604.tplinkdns.com`.
    *   Run development server listening on all interfaces (`python3 manage.py runserver 0.0.0.0:8000`).
25. **Mobile UI Improvement (User Dashboard):**
    *   Modified `templates/listings/user/ad_list_table.html` to use Bootstrap cards instead of a table for a better mobile experience.

## Mermaid Diagram (Simplified Flow)

```mermaid
graph LR
    subgraph User Interaction
        A[User Browser] --> B{Django App};
    end

    subgraph Django App
        B -- URL Routing --> C[Views];
        C -- Uses --> D[Forms];
        C -- Interacts with --> E[Models];
        E -- CRUD --> F[SQLite DB];
        C -- Renders --> G[Templates + Bootstrap];
    end

    subgraph Key Features
        H(Authentication) --> C;
        I(Ad Posting) --> C;
        J(Ad Display) --> C;
        K(Admin Tools) --> C;
        L(Category Mgmt) --> K;
        M(Ad Approval) --> K;
        N(User Mgmt) --> K;
    end

    G --> A;

    style F fill:#lightgrey,stroke:#333,stroke-width:2px
    style K fill:#lightblue,stroke:#333,stroke-width:2px