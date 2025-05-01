from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'ads', api_views.AdViewSet)
router.register(r'categories', api_views.CategoryViewSet)
router.register(r'subcategories', api_views.SubCategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
