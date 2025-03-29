# Classified Web Application Plan (Django + SQLite)

## Website Functionality Summary

This application provides a platform for users to post and browse classified advertisements. Key features include:

*   **User Authentication:** Secure user registration, login, and logout capabilities.
*   **Ad Listings:**
    *   Public homepage displaying all approved advertisements.
    *   **Homepage Filtering:** Keyword search (title/description), Category filter, dynamic Subcategory filter, Reset button.
    *   Detailed view page for each individual ad.
*   **User Ad Management:**
    *   Registered users can create new advertisements (submitted for admin approval).
    *   **Pricing Options:** Ads can have Fixed Price, Per Hour rate, Negotiable price, or be Free. Price field shown/required conditionally.
    *   A personal dashboard allows users to view the status (pending, approved, denied) of their ads.
    *   Users can edit or delete their own advertisements.
    *   The user's ad list is presented in a mobile-friendly card format.
*   **Moderator Features:**
    *   Users can be assigned to a "Moderators" group by admins.
    *   Moderators can access Ad Management to approve/deny selected pending ads.
    *   Moderators can flag users (providing a reason) for admin review.
*   **Admin Dashboard & Tools:**
    *   A restricted admin section (`/manage/`) for site management.
    *   **Mobile-Friendly UI:** Admin list views are responsive (table/cards).
    *   Full CRUD management for ad Categories and Subcategories (Superuser only).
    *   Comprehensive ad management: View all ads, approve or deny pending ads (individually by Mods/Admins, bulk by Admins).
    *   User management: View users, ban/unban, assign/remove Moderator role (Superuser only).
    *   **Flag Review:** Admins can review user flags submitted by moderators and ban users accordingly (Superuser only).
*   **Deployment Configuration:**
    *   Configured to be accessible over the network via `0.0.0.0:8000`.
    *   Firewall rules updated to allow traffic on port 8000.
    *   Domain `hung0604.tplinkdns.com` and `127.0.0.1`, `localhost` added to allowed hosts.

---

## Phase 1: Project Setup & Core Models

1.  **Initialize Django Project:** (Done)
2.  **Define Database Models (`listings/models.py`):**
    *   `Category`: `name`, `slug`, `description`. (Done)
    *   `SubCategory`: `name`, `slug`, `description`, `category`. (Done)
    *   `Ad`: `title`, `description`, `price_type` (choices), `price` (optional Decimal), `location` (optional), `category`, `subcategory`, `author`, `status`, `created_at`, `updated_at`. (Updated)
3.  **Database Migrations:** (Done)
4.  **Create Superuser (Admin):** (Done)

## Phase 2: User Authentication & Basic Views

5.  **Setup Authentication URLs:** (Done)
6.  **Create Basic Templates:** (Done)
7.  **Create Basic Views (`listings/views.py`):** (Done)
8.  **Configure URLs (`listings/urls.py`, main `urls.py`):** (Done)

## Phase 3: Ad Posting & Display

9.  **Ad Creation Form (`listings/forms.py`):** (Done)
10. **Ad Creation View (`listings/views.py`):** (Done)
11. **Ad Detail View (`listings/views.py` & Template):** (Done)
12. **Update Homepage View:** (Done)
13. **User Dashboard:** (Done)
14. **Update URLs:** (Done)

## Phase 4: Admin Tools Page

15. **Admin Access Control:** (Done - using `SuperuserRequiredMixin`)
16. **Category/SubCategory Management:** (Done)
17. **Ad Management View:** (Done)
18. **User Management View:** (Done - Ban/Unban)
19. **"TOOLS" Page Structure:** (Done - Renamed to `/manage/`)
20. **Update URLs:** (Done)

## Phase 5: Refinement & Styling

21. **Bootstrap Integration:** (Done)
22. **Styling:** (Ongoing)
23. **Testing:** (Ongoing)

## Phase 6: Deployment & Mobile UI Enhancement

24. **Network Accessibility:** (Done - `ALLOWED_HOSTS` updated)
25. **Mobile UI Improvement (User Dashboard):** (Done)

## Phase 7: Homepage Filtering & Ad Pricing

26. **Homepage Filtering:**
    *   Update `HomePageView` (`get_queryset`, `get_context_data`) to handle `q`, `category`, `subcategory` GET parameters.
    *   Update `home.html` template with filter form (Keyword, Category select, Subcategory select, Reset button).
    *   Add JavaScript to `home.html` for dynamic subcategory loading via `/api/subcategories/`.
    *   Update pagination links to preserve filters.
27. **Ad Pricing Options:**
    *   Add `price_type` field (CharField with choices: fixed, per_hour, negotiable, free) to `Ad` model.
    *   Run `makemigrations` and `migrate`.
    *   Update `AdForm` (`listings/forms.py`):
        *   Include `price_type` (use `RadioSelect` widget).
        *   Add `clean()` method to require `price` for fixed/per_hour and clear it for negotiable/free.
    *   Update `ad_form.html` template:
        *   Render `price_type` radio buttons.
        *   Add JavaScript to show/hide price field based on `price_type`.
    *   Update `ad_detail.html` and `home.html` to display price information according to `price_type`.

## Phase 8: Admin UI & Bug Fixes

28. **Fix `DisallowedHost`:** Add `127.0.0.1`, `localhost` to `ALLOWED_HOSTS`. (Done)
29. **Fix `NoReverseMatch`:** Update `admin_tools` URL name to `ads_management` in delete confirmation templates. (Done)
30. **Admin Mobile UI:**
    *   Refactor list view templates (`tools.html`, `ad_list.html`, `category_list.html`, `subcategory_list.html`, `user_management_list.html`) using responsive table/card pattern.
    *   Improve form templates (`category_form.html`, `subcategory_form.html`) styling for mobile.
31. **Fix Ad Form Rendering:** Remove commented-out image field from `ad_form.html`. (Done)

## Phase 9: Moderator Role & User Flagging

32. **Moderator Group & Permissions:**
    *   Manually create "Moderators" group in Django Admin.
    *   Assign permissions: `change_ad`, `view_ad`, `add_userflag`, `view_userflag`.
33. **`UserFlag` Model:**
    *   Create `UserFlag` model (`flagged_user`, `moderator`, `reason`, `details`, `created_at`, `status`).
    *   Run `makemigrations` and `migrate`.
34. **Update User Management:**
    *   Register `Group` and `UserFlag` models in `listings/admin.py`.
    *   Update `UserManagementListView` (`get_queryset` to annotate `is_moderator`, `post` to handle role assignment).
    *   Update `user_management_list.html` to show moderator status and add promote/demote buttons.
35. **Refine Access Control:**
    *   Create `RoleMiddleware` (`listings/middleware.py`) to add `is_moderator` to `request.user`.
    *   Add middleware to `settings.py`.
    *   Update `AdminAdListView` to use `UserPassesTestMixin` checking `is_superuser` or `is_moderator`.
    *   Update `ad_list.html` to hide bulk "Approve/Deny All" buttons for moderators.
36. **Implement User Flagging:**
    *   Add "Flag User" button to `ad_detail.html` (visible to moderators, not for self).
    *   Create `UserFlagForm` (`listings/forms.py`).
    *   Create `FlagUserView` (`listings/views.py`) (requires moderator, sets fields, prevents self/superuser flag).
    *   Add URL pattern for `flag_user`.
    *   Create `flag_user_form.html` template.
37. **Implement Flag Review:**
    *   Create `FlaggedUserListView` (`listings/views.py`) (superuser only, lists pending flags, handles banning).
    *   Create `flagged_user_list.html` template (displays flags, includes bulk/single ban actions).
    *   Add URL pattern for `flagged_user_list`.
    *   Update `AdsManagementView` and `tools.html` to link to review page and show pending count.
    *   Create `pagination.html` partial.

## Mermaid Diagram (Updated - High Level)

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
        B -- Processes --> MW[Middleware];
    end

    subgraph Key Features
        H(Authentication) --> C;
        I(Ad Posting/Mgmt) --> C;
        J(Ad Display/Filter) --> C;
        K(Admin Tools) --> C;
        MOD(Moderator Tools) --> C;
        L(Category/Subcat Mgmt) --> K;
        M(Ad Approval) -- Admin/Mod --> K & MOD;
        N(User Mgmt/Roles) --> K;
        FLAG(User Flagging) --> MOD;
        REV(Flag Review/Ban) --> K;
    end

    G --> A;
    MW --> C;

    style F fill:#lightgrey,stroke:#333,stroke-width:2px
    style K fill:#lightblue,stroke:#333,stroke-width:2px
    style MOD fill:#lightyellow,stroke:#333,stroke-width:2px