# User Test Cases (Playwright MCP)

This document outlines test cases for regular user functionalities of the classifieds application, executable using the Playwright MCP server.

**Base URL:** `https://rauma24h.com`

**Note:** These tests assume the application is running and accessible at the base URL.

## Logged-Out User Test Cases

### Test Case 1.1: Homepage Load and Content Verification

**Objective:** Verify that the homepage loads correctly and displays initial content for logged-out users.
**Steps:**
1. Navigate to the base URL (`/`).
2. Verify the presence of key elements: site title ("Classifieds"), "Login" link, "Sign Up" link, welcome message, search/filter form, and a list of approved ads (if any exist).
**Expected Outcome:** The homepage loads without errors, and the expected elements are visible.

### Test Case 1.2: Search Ads by Keyword

**Objective:** Test searching for ads using a keyword.
**Steps:**
1. Navigate to the base URL (`/`).
2. Enter a keyword in the "Keyword" search input.
3. Click the "Filter" button.
4. Verify that the displayed ads match the keyword (e.g., check ad titles or descriptions).
**Expected Outcome:** The page updates to show only ads containing the entered keyword.

### Test Case 1.3: Search Ads by Category

**Objective:** Test filtering ads by selecting a category.
**Steps:**
1. Navigate to the base URL (`/`).
2. Select a category from the "Category" dropdown.
3. Click the "Filter" button.
4. Verify that the displayed ads belong to the selected category.
**Expected Outcome:** The page updates to show only ads belonging to the selected category.

### Test Case 1.4: Search Ads by Subcategory

**Objective:** Test filtering ads by selecting a subcategory.
**Steps:**
1. Navigate to the base URL (`/`).
2. Select a category from the "Category" dropdown (ensure it has subcategories).
3. Select a subcategory from the "Subcategory" dropdown (which should become enabled).
4. Click the "Filter" button.
5. Verify that the displayed ads belong to the selected subcategory within the chosen category.
**Expected Outcome:** The page updates to show only ads belonging to the selected subcategory.

### Test Case 1.5: View Ad Detail Page

**Objective:** Test navigating to and viewing the details of a single ad.
**Steps:**
1. Navigate to the base URL (`/`).
2. Click the "View Details" button for an ad.
3. Verify that the ad detail page loads and displays the full information for that ad (title, description, price, category, location, author, etc.).
**Expected Outcome:** The ad detail page loads correctly and shows the complete details of the selected ad.

### Test Case 1.6: Access Login Page

**Objective:** Verify that the login page is accessible.
**Steps:**
1. Navigate to the base URL (`/`).
2. Click the "Login" link in the navigation.
3. Verify that the login page loads with the login form.
**Expected Outcome:** The login page loads successfully.

### Test Case 1.7: Access Sign Up Page

**Objective:** Verify that the sign up page is accessible.
**Steps:**
1. Navigate to the base URL (`/`).
2. Click the "Sign Up" link in the navigation.
3. Verify that the sign up page loads with the registration form.
**Expected Outcome:** The sign up page loads successfully.

### Test Case 1.8: User Registration

**Objective:** Test the user registration process.
**Steps:**
1. Navigate to the Sign Up page (`/signup/`).
2. Fill out the username, email, password, and password confirmation fields with valid, unique data.
3. Click the "Sign Up" button.
4. Verify redirection to the login page and the presence of a success message ("Account created successfully. Please log in.").
**Expected Outcome:** A new user account is created, and the user is redirected to the login page with a success message.

## Logged-In User Test Cases

**Prerequisite:** User is logged in. (Test Case 2.1 covers login).

### Test Case 2.1: User Login

**Objective:** Test the user login process.
**Steps:**
1. Navigate to the Login page (`/accounts/login/`).
2. Fill out the username and password fields with valid user credentials.
3. Click the "Login" button.
4. Verify redirection to the homepage and that the navigation links change to show logged-in options ("Hi [username]!", "My Dashboard", "Post Ad", "Logout").
**Expected Outcome:** The user is successfully logged in and redirected to the homepage with logged-in navigation.

### Test Case 2.2: Access User Dashboard

**Objective:** Verify that the user dashboard is accessible and displays the user's ads.
**Steps:**
1. Log in as a user.
2. Click the "My Dashboard" link in the navigation.
3. Verify that the user dashboard page loads and displays a list of the logged-in user's ads (if any).
**Expected Outcome:** The user dashboard loads successfully and shows the user's advertisements.

### Test Case 2.3: Post a New Ad

**Objective:** Test the process of creating and submitting a new ad.
**Steps:**
1. Log in as a user.
2. Click the "Post Ad" link in the navigation.
3. Fill out the required fields in the ad creation form (Title, Description, Category, Price Type, Price/Negotiable status, Location). Select a category and subcategory.
4. Click the "Submit Ad for Approval" button.
5. Verify redirection to the homepage.
6. Navigate to the user dashboard (`/dashboard/`).
7. Verify that the newly created ad is listed on the dashboard with a "Pending" status.
**Expected Outcome:** A new ad is successfully submitted and appears on the user dashboard with a pending status.

### Test Case 2.4: Update an Existing Ad

**Objective:** Test updating an existing ad from the user dashboard.
**Steps:**
1. Log in as a user who has existing ads.
2. Navigate to the user dashboard (`/dashboard/`).
3. Click the "Edit" link for one of the user's ads.
4. Verify that the ad update form loads with the existing ad details pre-filled.
5. Modify one or more fields in the form.
6. Click the "Submit Ad for Approval" button.
7. Verify redirection to the user dashboard.
8. Verify that the updated ad is listed on the dashboard and its status is set back to "Pending".
**Expected Outcome:** The ad is successfully updated, and its status is set to pending.

### Test Case 2.5: Delete an Existing Ad

**Objective:** Test deleting an existing ad from the user dashboard.
**Steps:**
1. Log in as a user who has existing ads.
2. Navigate to the user dashboard (`/dashboard/`).
3. Click the "Delete" link for one of the user's ads.
4. Verify that the ad confirmation delete page loads.
5. Click the "Confirm Delete" button.
6. Verify redirection to the user dashboard.
7. Verify that the deleted ad is no longer listed on the dashboard.
**Expected Outcome:** The ad is successfully deleted and removed from the user dashboard.

### Test Case 2.6: User Logout

**Objective:** Test the user logout process.
**Steps:**
1. Log in as a user.
2. Click the "Logout" button in the navigation.
3. Verify redirection to the homepage and that the navigation links change back to logged-out options ("Login", "Sign Up").
**Expected Outcome:** The user is successfully logged out.
