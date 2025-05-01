# Admin Test Cases (Playwright MCP)

This document outlines test cases for admin functionalities of the classifieds application, executable using the Playwright MCP server.

**Base URL:** `https://rauma24h.com`
**Admin Credentials:**
- Username: `kevin9999`
- Password: `Hung889900@@`

**Note:** These tests assume the application is running and accessible at the base URL, and that the admin user with the specified credentials exists and has superuser privileges.

## Admin Login

### Test Case 3.1: Admin Login

**Objective:** Test the admin user login process.
**Steps:**
1. Navigate to the Login page (`/accounts/login/`).
2. Fill out the username field with `kevin9999`.
3. Fill out the password field with `Hung889900@@`.
4. Click the "Login" button.
5. Verify redirection to the homepage and that the navigation links include admin options (e.g., "Admin Tools" or similar, depending on implementation).
**Expected Outcome:** The admin user is successfully logged in and redirected to the homepage with admin navigation options.

## Admin Tools and Ad Management

**Prerequisite:** Admin user is logged in.

### Test Case 3.2: Access Admin Tools Page

**Objective:** Verify that the Admin Tools page is accessible to superusers.
**Steps:**
1. Log in as the admin user (`kevin9999`).
2. Navigate to the Admin Tools page (URL needs to be confirmed, likely `/admin/tools/` or similar based on `AdsManagementView`).
3. Verify that the Admin Tools page loads and displays links to various management sections (Ads, Categories, Users, Flags).
**Expected Outcome:** The Admin Tools page loads successfully with links to management sections.

### Test Case 3.3: View All Ads (Admin List)

**Objective:** Verify that the admin can view a list of all ads, regardless of status.
**Steps:**
1. Log in as the admin user.
2. Navigate to the Admin Ad List page (URL needs to be confirmed, likely `/admin/ads/` or similar based on `AdminAdListView`).
3. Verify that the page loads and displays a list of all ads, including their status (Pending, Approved, Denied).
**Expected Outcome:** The Admin Ad List page loads and shows all ads with their statuses.

### Test Case 3.4: Filter Ads by Status (Pending)

**Objective:** Test filtering the admin ad list to show only pending ads.
**Steps:**
1. Log in as the admin user.
2. Navigate to the Admin Ad List page.
3. Click the filter option for "Pending" status.
4. Verify that the displayed ads have a "Pending" status.
**Expected Outcome:** The ad list is filtered to show only pending ads.

### Test Case 3.5: Filter Ads by Status (Approved)

**Objective:** Test filtering the admin ad list to show only approved ads.
**Steps:**
1. Log in as the admin user.
2. Navigate to the Admin Ad List page.
3. Click the filter option for "Approved" status.
4. Verify that the displayed ads have an "Approved" status.
**Expected Outcome:** The ad list is filtered to show only approved ads.

### Test Case 3.6: Filter Ads by Status (Denied)

**Objective:** Test filtering the admin ad list to show only denied ads.
**Steps:**
1. Log in as the admin user.
2. Navigate to the Admin Ad List page.
3. Click the filter option for "Denied" status.
4. Verify that the displayed ads have a "Denied" status.
**Expected Outcome:** The ad list is filtered to show only denied ads.

### Test Case 3.7: Approve Selected Ads (Bulk Action)

**Objective:** Test approving multiple selected pending ads.
**Steps:**
1. Log in as the admin user.
2. Navigate to the Admin Ad List page, filtered or showing pending ads.
3. Select multiple pending ads using checkboxes.
4. Select the "Approve Selected" action from the bulk actions dropdown/buttons.
5. Confirm the action if prompted.
6. Verify that the selected ads' status changes to "Approved" (may require refreshing the list or navigating back).
**Expected Outcome:** The selected pending ads are successfully approved.

### Test Case 3.8: Deny Selected Ads (Bulk Action)

**Objective:** Test denying multiple selected pending ads.
**Steps:**
1. Log in as the admin user.
2. Navigate to the Admin Ad List page, filtered or showing pending ads.
3. Select multiple pending ads using checkboxes.
4. Select the "Deny Selected" action from the bulk actions dropdown/buttons.
5. Confirm the action if prompted.
6. Verify that the selected ads' status changes to "Denied" (may require refreshing the list or navigating back).
**Expected Outcome:** The selected pending ads are successfully denied.

### Test Case 3.9: Approve All Pending Ads (Bulk Action)

**Objective:** Test approving all pending ads.
**Steps:**
1. Log in as the admin user.
2. Navigate to the Admin Ad List page, filtered or showing pending ads.
3. Select the "Approve All Pending" action from the bulk actions dropdown/buttons.
4. Confirm the action if prompted.
5. Verify that all pending ads' status changes to "Approved" and the pending count updates.
**Expected Outcome:** All pending ads are successfully approved.

### Test Case 3.10: Deny All Pending Ads (Bulk Action)

**Objective:** Test denying all pending ads.
**Steps:**
1. Log in as the admin user.
2. Navigate to the Admin Ad List page, filtered or showing pending ads.
3. Select the "Deny All Pending" action from the bulk actions dropdown/buttons.
4. Confirm the action if prompted.
5. Verify that all pending ads' status changes to "Denied" and the pending count updates.
**Expected Outcome:** All pending ads are successfully denied.

## Category Management

**Prerequisite:** Admin user is logged in.

### Test Case 3.11: View Categories List

**Objective:** Verify that the admin can view the list of categories.
**Steps:**
1. Log in as the admin user.
2. Navigate to the Category List page (URL needs to be confirmed, likely `/admin/categories/` or similar based on `CategoryListView`).
3. Verify that the page loads and displays a list of existing categories.
**Expected Outcome:** The Category List page loads and shows the categories.

### Test Case 3.12: Create New Category

**Objective:** Test creating a new category.
**Steps:**
1. Log in as the admin user.
2. Navigate to the Category Create page (URL needs to be confirmed, likely `/admin/categories/new/` or similar based on `CategoryCreateView`).
3. Fill out the form with a new category name.
4. Click the submit button.
5. Verify redirection to the Category List page and the presence of a success message.
6. Verify that the new category appears in the list.
**Expected Outcome:** A new category is successfully created and listed.

### Test Case 3.13: Update Category

**Objective:** Test updating an existing category.
**Steps:**
1. Log in as the admin user.
2. Navigate to the Category List page.
3. Click the "Edit" link for a category.
4. Verify that the Category Update form loads with the existing details.
5. Modify the category name.
6. Click the submit button.
7. Verify redirection to the Category List page and the presence of a success message.
8. Verify that the category name is updated in the list.
**Expected Outcome:** The category is successfully updated.

### Test Case 3.14: Delete Category

**Objective:** Test deleting an existing category.
**Steps:**
1. Log in as the admin user.
2. Navigate to the Category List page.
3. Click the "Delete" link for a category.
4. Verify that the Category Confirmation Delete page loads.
5. Click the "Confirm Delete" button.
6. Verify redirection to the Category List page and the presence of a success message.
7. Verify that the category is no longer in the list.
**Expected Outcome:** The category is successfully deleted.

## Subcategory Management

**Prerequisite:** Admin user is logged in.

### Test Case 3.15: View Subcategories List

**Objective:** Verify that the admin can view the list of subcategories.
**Steps:**
1. Log in as the admin user.
2. Navigate to the Subcategory List page (URL needs to be confirmed, likely `/admin/subcategories/` or similar based on `SubCategoryListView`).
3. Verify that the page loads and displays a list of existing subcategories.
**Expected Outcome:** The Subcategory List page loads and shows the subcategories.

### Test Case 3.16: Create New Subcategory

**Objective:** Test creating a new subcategory.
**Steps:**
1. Log in as the admin user.
2. Navigate to the Subcategory Create page (URL needs to be confirmed, likely `/admin/subcategories/new/` or similar based on `SubCategoryCreateView`).
3. Fill out the form with a new subcategory name and select a parent category.
4. Click the submit button.
5. Verify redirection to the Subcategory List page and the presence of a success message.
6. Verify that the new subcategory appears in the list.
**Expected Outcome:** A new subcategory is successfully created and listed.

### Test Case 3.17: Update Subcategory

**Objective:** Test updating an existing subcategory.
**Steps:**
1. Log in as the admin user.
2. Navigate to the Subcategory List page.
3. Click the "Edit" link for a subcategory.
4. Verify that the Subcategory Update form loads with the existing details.
5. Modify the subcategory name or parent category.
6. Click the submit button.
7. Verify redirection to the Subcategory List page and the presence of a success message.
8. Verify that the subcategory details are updated in the list.
**Expected Outcome:** The subcategory is successfully updated.

### Test Case 3.18: Delete Subcategory

**Objective:** Test deleting an existing subcategory.
**Steps:**
1. Log in as the admin user.
2. Navigate to the Subcategory List page.
3. Click the "Delete" link for a subcategory.
4. Verify that the Subcategory Confirmation Delete page loads.
5. Click the "Confirm Delete" button.
6. Verify redirection to the Subcategory List page and the presence of a success message.
7. Verify that the subcategory is no longer in the list.
**Expected Outcome:** The subcategory is successfully deleted.

## User Management

**Prerequisite:** Admin user is logged in.

### Test Case 3.19: View User Management List

**Objective:** Verify that the admin can view the list of users for management.
**Steps:**
1. Log in as the admin user.
2. Navigate to the User Management List page (URL needs to be confirmed, likely `/admin/users/` or similar based on `UserManagementListView`).
3. Verify that the page loads and displays a list of users.
**Expected Outcome:** The User Management List page loads and shows the users.

### Test Case 3.20: Ban a User

**Objective:** Test banning (deactivating) a user.
**Steps:**
1. Log in as the admin user.
2. Navigate to the User Management List page.
3. Find a non-superuser user in the list.
4. Click the "Ban" action for that user.
5. Confirm the action if prompted.
6. Verify that the user's status changes to banned/inactive (may require refreshing the list).
**Expected Outcome:** The user is successfully banned (deactivated).

### Test Case 3.21: Unban a User

**Objective:** Test unbanning (activating) a user.
**Steps:**
1. Log in as the admin user.
2. Navigate to the User Management List page.
3. Find a banned/inactive user in the list.
4. Click the "Unban" action for that user.
5. Confirm the action if prompted.
6. Verify that the user's status changes to active (may require refreshing the list).
**Expected Outcome:** The user is successfully unbanned (activated).

### Test Case 3.22: Assign Moderator Role

**Objective:** Test assigning the moderator role to a user.
**Steps:**
1. Log in as the admin user.
2. Navigate to the User Management List page.
3. Find a non-superuser user who is not a moderator.
4. Click the "Make Moderator" action for that user.
5. Confirm the action if prompted.
6. Verify that the user is marked as a moderator in the list (may require refreshing).
**Expected Outcome:** The user is successfully assigned the moderator role.

### Test Case 3.23: Remove Moderator Role

**Objective:** Test removing the moderator role from a user.
**Steps:**
1. Log in as the admin user.
2. Navigate to the User Management List page.
3. Find a user who is a moderator (but not a superuser).
4. Click the "Remove Moderator" action for that user.
5. Confirm the action if prompted.
6. Verify that the user is no longer marked as a moderator in the list (may require refreshing).
**Expected Outcome:** The moderator role is successfully removed from the user.

## Flagged User Management

**Prerequisite:** Admin user is logged in, and there are pending user flags.

### Test Case 3.24: View Flagged User List

**Objective:** Verify that the admin can view the list of pending user flags.
**Steps:**
1. Log in as the admin user.
2. Ensure there are pending user flags (this might require a moderator to flag a user first).
3. Navigate to the Flagged User List page (URL needs to be confirmed, likely `/admin/flags/` or similar based on `FlaggedUserListView`).
4. Verify that the page loads and displays a list of pending user flags.
**Expected Outcome:** The Flagged User List page loads and shows pending flags.

### Test Case 3.25: Ban User from Flagged List (Bulk Action)

**Objective:** Test banning users based on selected pending flags.
**Steps:**
1. Log in as the admin user.
2. Navigate to the Flagged User List page.
3. Select one or more pending flags using checkboxes.
4. Select the "Ban Selected" action from the bulk actions dropdown/buttons.
5. Confirm the action if prompted.
6. Verify that the corresponding users are banned (deactivated) and the selected flags are marked as resolved.
**Expected Outcome:** The users associated with the selected flags are banned, and the flags are resolved.

### Test Case 3.26: Ban All Flagged Users (Bulk Action)

**Objective:** Test banning all users with pending flags.
**Steps:**
1. Log in as the admin user.
2. Navigate to the Flagged User List page.
3. Select the "Ban All Pending" action from the bulk actions dropdown/buttons.
4. Confirm the action if prompted.
5. Verify that all users with pending flags are banned (deactivated) and all pending flags are marked as resolved.
**Expected Outcome:** All users with pending flags are banned, and all pending flags are resolved.
