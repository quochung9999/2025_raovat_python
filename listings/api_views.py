from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import Ad, Category, SubCategory
from .serializers import AdSerializer, CategorySerializer, SubCategorySerializer

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows categories to be viewed.
    """
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [AllowAny] # Categories are publicly viewable

class SubCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows subcategories to be viewed.
    """
    queryset = SubCategory.objects.all().order_by('name')
    serializer_class = SubCategorySerializer
    permission_classes = [AllowAny] # Subcategories are publicly viewable

class AdViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ads to be viewed or edited.
    """
    queryset = Ad.objects.filter(status=Ad.STATUS_APPROVED).order_by('-created_at')
    serializer_class = AdSerializer
    permission_classes = [IsAuthorOrAdminOrModerator] # Use custom permission

    def get_queryset(self):
        """
        Optionally restricts the returned ads to a given user,
        by filtering against a `author_id` query parameter in the URL.
        Also allows filtering by status for authenticated users.
        """
        queryset = Ad.objects.all().order_by('-created_at')

        # Allow filtering by author for authenticated users
        author_id = self.request.query_params.get('author_id', None)
        if author_id is not None and self.request.user.is_authenticated:
            queryset = queryset.filter(author_id=author_id)
        elif not self.request.user.is_authenticated:
             # For unauthenticated users, only show approved ads
             queryset = queryset.filter(status=Ad.STATUS_APPROVED)

        # Allow filtering by status for authenticated users (e.g., admin/moderator)
        status = self.request.query_params.get('status', None)
        if status is not None and self.request.user.is_authenticated:
             # Ensure the requested status is valid
             if status in [Ad.STATUS_PENDING, Ad.STATUS_APPROVED, Ad.STATUS_DENIED]:
                 queryset = queryset.filter(status=status)
             # Note: We might want stricter permissions here for viewing pending/denied

        return queryset

    def perform_create(self, serializer):
        """Assign the current user as the author and set status to pending on creation."""
        serializer.save(author=self.request.user, status=Ad.STATUS_PENDING)

    def perform_update(self, serializer):
        """Set status back to pending when an ad is updated."""
        serializer.save(status=Ad.STATUS_PENDING)
