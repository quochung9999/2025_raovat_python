from django.urls import path
from . import views # Import views module directly for function view
from .views import (
    HomePageView, SignUpView, CreateAdView, AdDetailView,
    # Admin views
    AdsManagementView, AdminAdListView, UserManagementListView, FlaggedUserListView, # Added FlaggedUserListView
    # Category management views
    CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView,
    # Subcategory management views
    SubCategoryListView, SubCategoryCreateView, SubCategoryUpdateView, SubCategoryDeleteView,
    # User dashboard, ad update, and ad delete views
    UserDashboardView, UpdateAdView, DeleteAdView,
    # Moderator views
    FlagUserView, # Import FlagUserView
)

urlpatterns = [
    # Public URLs
    path('', HomePageView.as_view(), name='home'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('ad/new/', CreateAdView.as_view(), name='ad_create'),
    path('ad/<int:pk>/', AdDetailView.as_view(), name='ad_detail'),
    
    # User URLs
    path('dashboard/', UserDashboardView.as_view(), name='user_dashboard'),
    path('dashboard/ad/<int:pk>/edit/', UpdateAdView.as_view(), name='ad_update'),
    path('dashboard/ad/<int:pk>/delete/', DeleteAdView.as_view(), name='ad_delete'), # Add delete URL

    # Moderator URLs
    path('flag-user/<int:user_id>/', FlagUserView.as_view(), name='flag_user'), # Add flag user URL

    # Admin URLs - Prefix changed from 'tools/' to 'manage/'
    path('manage/', AdsManagementView.as_view(), name='ads_management'), # Renamed from admin_tools
    path('manage/ads/', AdminAdListView.as_view(), name='admin_ad_list'),
    path('manage/users/', UserManagementListView.as_view(), name='user_management_list'), # Add user management URL
    path('manage/flags/', FlaggedUserListView.as_view(), name='flagged_user_list'), # Add flag review URL

    # Category management URLs
    path('manage/categories/', CategoryListView.as_view(), name='category_list'),
    path('manage/categories/new/', CategoryCreateView.as_view(), name='category_create'),
    path('manage/categories/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category_update'),
    path('manage/categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),
    
    # Subcategory management URLs
    path('manage/subcategories/', SubCategoryListView.as_view(), name='subcategory_list'),
    path('manage/subcategories/new/', SubCategoryCreateView.as_view(), name='subcategory_create'),
    path('manage/subcategories/<int:pk>/edit/', SubCategoryUpdateView.as_view(), name='subcategory_update'),
    path('manage/subcategories/<int:pk>/delete/', SubCategoryDeleteView.as_view(), name='subcategory_delete'),
    
    # API URLs
    path('api/subcategories/<int:category_id>/', views.get_subcategories, name='api_get_subcategories'),
]