# Backend API Test Cases

This document outlines test cases for the backend API endpoints of the classifieds project.

**Base URL:** `/api/`

**Note:** These tests require the backend server to be running and accessible. Authentication for write operations on Ads is required.

## Ad API Test Cases (`/api/ads/`)

### Test Case API 1.1: List Approved Ads (Unauthenticated)

**Objective:** Verify that unauthenticated users can list approved ads.
**Endpoint:** `GET /api/ads/`
**Expected Status Code:** 200 OK
**Expected Outcome:** Returns a list of ads with `status=approved`.

### Test Case API 1.2: List All Ads (Authenticated)

**Objective:** Verify that authenticated users can list all ads (including pending/denied if authorized).
**Endpoint:** `GET /api/ads/`
**Authentication:** Required
**Expected Status Code:** 200 OK
**Expected Outcome:** Returns a list of all ads, potentially including pending/denied based on user permissions.

### Test Case API 1.3: Retrieve Approved Ad (Unauthenticated)

**Objective:** Verify that unauthenticated users can retrieve details of an approved ad.
**Endpoint:** `GET /api/ads/{id}/` (where {id} is an approved ad ID)
**Expected Status Code:** 200 OK
**Expected Outcome:** Returns the details of the specified approved ad.

### Test Case API 1.4: Retrieve Ad (Authenticated)

**Objective:** Verify that authenticated users can retrieve details of any ad they are authorized to view (e.g., their own pending/denied ads, or all ads for admin/moderator).
**Endpoint:** `GET /api/ads/{id}/` (where {id} is an ad ID)
**Authentication:** Required
**Expected Status Code:** 200 OK
**Expected Outcome:** Returns the details of the specified ad if the user is authorized.

### Test Case API 1.5: Attempt Retrieve Pending/Denied Ad (Unauthenticated)

**Objective:** Verify that unauthenticated users cannot retrieve details of pending or denied ads.
**Endpoint:** `GET /api/ads/{id}/` (where {id} is a pending or denied ad ID)
**Expected Status Code:** 404 Not Found or 403 Forbidden (depending on exact permission implementation)
**Expected Outcome:** Returns an error indicating the ad was not found or access is forbidden.

### Test Case API 1.6: Create New Ad (Authenticated)

**Objective:** Test creating a new ad via the API.
**Endpoint:** `POST /api/ads/`
**Authentication:** Required
**Request Body:** JSON object with valid ad data (title, description, category_id, subcategory_id, price_type, price, location).
**Expected Status Code:** 201 Created
**Expected Outcome:** A new ad is created with the logged-in user as the author and status set to "pending". Returns the details of the newly created ad.

### Test Case API 1.7: Attempt Create Ad (Unauthenticated)

**Objective:** Verify that unauthenticated users cannot create ads.
**Endpoint:** `POST /api/ads/`
**Authentication:** Not Required
**Request Body:** JSON object with valid ad data.
**Expected Status Code:** 401 Unauthorized
**Expected Outcome:** Returns an authentication required error.

### Test Case API 1.8: Update Own Ad (Authenticated, Author)

**Objective:** Test updating an ad as its author.
**Endpoint:** `PUT /api/ads/{id}/` (where {id} is the author's ad ID)
**Authentication:** Required (as the ad's author)
**Request Body:** JSON object with updated ad data.
**Expected Status Code:** 200 OK
**Expected Outcome:** The ad is successfully updated, and its status is set back to "pending".

### Test Case API 1.9: Partially Update Own Ad (Authenticated, Author)

**Objective:** Test partially updating an ad as its author.
**Endpoint:** `PATCH /api/ads/{id}/` (where {id} is the author's ad ID)
**Authentication:** Required (as the ad's author)
**Request Body:** JSON object with partial ad data to update.
**Expected Status Code:** 200 OK
**Expected Outcome:** The ad is successfully partially updated, and its status is set back to "pending".

### Test Case API 1.10: Delete Own Ad (Authenticated, Author)

**Objective:** Test deleting an ad as its author.
**Endpoint:** `DELETE /api/ads/{id}/` (where {id} is the author's ad ID)
**Authentication:** Required (as the ad's author)
**Expected Status Code:** 204 No Content
**Expected Outcome:** The ad is successfully deleted.

### Test Case API 1.11: Attempt Update Another User's Ad (Authenticated, Not Author/Admin/Moderator)

**Objective:** Verify that a regular authenticated user cannot update another user's ad.
**Endpoint:** `PUT /api/ads/{id}/` (where {id} is another user's ad ID)
**Authentication:** Required (as a regular user)
**Request Body:** JSON object with updated ad data.
**Expected Status Code:** 403 Forbidden
**Expected Outcome:** Returns a permission denied error.

### Test Case API 1.12: Attempt Delete Another User's Ad (Authenticated, Not Author/Admin/Moderator)

**Objective:** Verify that a regular authenticated user cannot delete another user's ad.
**Endpoint:** `DELETE /api/ads/{id}/` (where {id} is another user's ad ID)
**Authentication:** Required (as a regular user)
**Expected Status Code:** 403 Forbidden
**Expected Outcome:** Returns a permission denied error.

### Test Case API 1.13: Update Any Ad (Authenticated, Admin/Moderator)

**Objective:** Test updating any ad as an admin or moderator.
**Endpoint:** `PUT /api/ads/{id}/` (where {id} is any ad ID)
**Authentication:** Required (as admin or moderator)
**Request Body:** JSON object with updated ad data.
**Expected Status Code:** 200 OK
**Expected Outcome:** The ad is successfully updated, and its status is set back to "pending".

### Test Case API 1.14: Delete Any Ad (Authenticated, Admin/Moderator)

**Objective:** Test deleting any ad as an admin or moderator.
**Endpoint:** `DELETE /api/ads/{id}/` (where {id} is any ad ID)
**Authentication:** Required (as admin or moderator)
**Expected Status Code:** 204 No Content
**Expected Outcome:** The ad is successfully deleted.

### Test Case API 1.15: Filter Ads by Author (Authenticated)

**Objective:** Test filtering ads by author ID using a query parameter.
**Endpoint:** `GET /api/ads/?author_id={author_id}` (where {author_id} is a user ID)
**Authentication:** Required
**Expected Status Code:** 200 OK
**Expected Outcome:** Returns a list of ads authored by the specified user.

### Test Case API 1.16: Filter Ads by Status (Authenticated)

**Objective:** Test filtering ads by status using a query parameter.
**Endpoint:** `GET /api/ads/?status={status}` (where {status} is 'pending', 'approved', or 'denied')
**Authentication:** Required
**Expected Status Code:** 200 OK
**Expected Outcome:** Returns a list of ads with the specified status.

## Category API Test Cases (`/api/categories/`)

### Test Case API 2.1: List Categories

**Objective:** Verify that categories can be listed via the API.
**Endpoint:** `GET /api/categories/`
**Expected Status Code:** 200 OK
**Expected Outcome:** Returns a list of all categories.

### Test Case API 2.2: Retrieve Category

**Objective:** Verify that a single category can be retrieved via the API.
**Endpoint:** `GET /api/categories/{id}/` (where {id} is a category ID)
**Expected Status Code:** 200 OK
**Expected Outcome:** Returns the details of the specified category.

## SubCategory API Test Cases (`/api/subcategories/`)

### Test Case API 3.1: List Subcategories

**Objective:** Verify that subcategories can be listed via the API.
**Endpoint:** `GET /api/subcategories/`
**Expected Status Code:** 200 OK
**Expected Outcome:** Returns a list of all subcategories.

### Test Case API 3.2: Retrieve Subcategory

**Objective:** Verify that a single subcategory can be retrieved via the API.
**Endpoint:** `GET /api/subcategories/{id}/` (where {id} is a subcategory ID)
**Expected Status Code:** 200 OK
**Expected Outcome:** Returns the details of the specified subcategory.
