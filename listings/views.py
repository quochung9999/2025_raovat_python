from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, DetailView, ListView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin # Import UserPassesTestMixin
from django.contrib.auth.models import User # Import User model
from django.contrib import messages
from django.http import JsonResponse # Import JsonResponse
from django.db.models import Q, Exists, OuterRef # Import Q, Exists, OuterRef
from django.contrib.auth.models import Group # Import Group model

# Add near other model imports
from .models import UserFlag
# Add near other form imports
from .forms import UserFlagForm

from .models import Ad, Category, SubCategory
from .forms import AdForm, CategoryForm, SubCategoryForm, CustomUserCreationForm
from .decorators import SuperuserRequiredMixin

# Create your views here.

class HomePageView(ListView):
    """
    Displays the homepage with a list of approved ads,
    allowing filtering by keyword, category, and subcategory.
    """
    model = Ad
    template_name = 'home.html'
    context_object_name = 'ad_list'
    paginate_by = 10

    def get_queryset(self):
        """
        Return approved ads, filtered by GET parameters, ordered by most recent.
        """
        queryset = Ad.objects.filter(status=Ad.STATUS_APPROVED)

        query = self.request.GET.get('q')
        category_id = self.request.GET.get('category')
        subcategory_id = self.request.GET.get('subcategory')

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )

        if category_id and category_id.isdigit():
            queryset = queryset.filter(category_id=category_id)

        if subcategory_id and subcategory_id.isdigit():
            queryset = queryset.filter(subcategory_id=subcategory_id)

        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        """
        Add categories and current filter values to the context.
        """
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.order_by('name')
        context['current_filters'] = {
            'q': self.request.GET.get('q', ''),
            'category': self.request.GET.get('category', ''),
            'subcategory': self.request.GET.get('subcategory', ''),
        }
        # Fetch subcategories if a category is selected, for pre-populating the subcategory dropdown
        # This helps if the page reloads with a category already selected
        category_id = self.request.GET.get('category')
        if category_id and category_id.isdigit():
             context['subcategories'] = SubCategory.objects.filter(category_id=category_id).order_by('name')
        else:
             context['subcategories'] = SubCategory.objects.none() # Empty queryset if no category selected

        return context

class SignUpView(CreateView):
    """
    Handles user registration.
    Uses our custom form for creating users with Bootstrap styling.
    Redirects to the login page upon successful signup.
    """
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login') # Redirect to login page after signup
    template_name = 'registration/signup.html'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Account created successfully. Please log in.")
        return response

class CreateAdView(LoginRequiredMixin, CreateView):
    """
    Handles the creation of new advertisements.
    Requires user to be logged in.
    Sets the author automatically and status to 'pending'.
    """
    model = Ad
    form_class = AdForm
    template_name = 'listings/ad_form.html' # We need to create this template
    success_url = reverse_lazy('home') # Redirect to homepage after successful creation

    def form_valid(self, form):
        """Assign the current user as the author and set status."""
        form.instance.author = self.request.user
        form.instance.status = Ad.STATUS_PENDING # Ensure status is pending
        return super().form_valid(form)

class AdDetailView(DetailView):
    """
    Displays the details of a single advertisement.
    Only shows ads that are 'approved'.
    """
    model = Ad
    template_name = 'listings/ad_detail.html'
    context_object_name = 'ad'

    def get_queryset(self):
        """
        Ensure only approved ads are shown to general users.
        Authors can see their own ads regardless of status.
        Admins can see all ads.
        """
        queryset = super().get_queryset()
        
        # If user is the author or admin, show the ad regardless of status
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser:
                return queryset  # Admin can see all ads
            
            # Author can see their own ads
            author_filter = queryset.filter(author=self.request.user)
            status_filter = queryset.filter(status=Ad.STATUS_APPROVED)
            return author_filter | status_filter  # Union of both querysets
            
        # For non-authenticated users, only show approved ads
        return queryset.filter(status=Ad.STATUS_APPROVED)

# Admin views for category management
class CategoryListView(SuperuserRequiredMixin, ListView):
    """
    Displays a list of all categories.
    Only accessible by superusers.
    """
    model = Category
    template_name = 'listings/admin/category_list.html'
    context_object_name = 'categories'

class CategoryCreateView(SuperuserRequiredMixin, CreateView):
    """
    Allows creation of new categories.
    Only accessible by superusers.
    """
    model = Category
    form_class = CategoryForm
    template_name = 'listings/admin/category_form.html'
    success_url = reverse_lazy('category_list')

    def form_valid(self, form):
        messages.success(self.request, "Category created successfully.")
        return super().form_valid(form)

class CategoryUpdateView(SuperuserRequiredMixin, UpdateView):
    """
    Allows updating existing categories.
    Only accessible by superusers.
    """
    model = Category
    form_class = CategoryForm
    template_name = 'listings/admin/category_form.html'
    success_url = reverse_lazy('category_list')

    def form_valid(self, form):
        messages.success(self.request, "Category updated successfully.")
        return super().form_valid(form)

class CategoryDeleteView(SuperuserRequiredMixin, DeleteView):
    """
    Allows deletion of categories.
    Only accessible by superusers.
    """
    model = Category
    template_name = 'listings/admin/category_confirm_delete.html'
    success_url = reverse_lazy('category_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Category deleted successfully.")
        return super().delete(request, *args, **kwargs)

# Admin views for subcategory management
class SubCategoryListView(SuperuserRequiredMixin, ListView):
    """
    Displays a list of all subcategories.
    Only accessible by superusers.
    """
    model = SubCategory
    template_name = 'listings/admin/subcategory_list.html'
    context_object_name = 'subcategories'

class SubCategoryCreateView(SuperuserRequiredMixin, CreateView):
    """
    Allows creation of new subcategories.
    Only accessible by superusers.
    """
    model = SubCategory
    form_class = SubCategoryForm
    template_name = 'listings/admin/subcategory_form.html'
    success_url = reverse_lazy('subcategory_list')

    def form_valid(self, form):
        messages.success(self.request, "Subcategory created successfully.")
        return super().form_valid(form)

class SubCategoryUpdateView(SuperuserRequiredMixin, UpdateView):
    """
    Allows updating existing subcategories.
    Only accessible by superusers.
    """
    model = SubCategory
    form_class = SubCategoryForm
    template_name = 'listings/admin/subcategory_form.html'
    success_url = reverse_lazy('subcategory_list')

    def form_valid(self, form):
        messages.success(self.request, "Subcategory updated successfully.")
        return super().form_valid(form)

class SubCategoryDeleteView(SuperuserRequiredMixin, DeleteView):
    """
    Allows deletion of subcategories.
    Only accessible by superusers.
    """
    model = SubCategory
    template_name = 'listings/admin/subcategory_confirm_delete.html'
    success_url = reverse_lazy('subcategory_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Subcategory deleted successfully.")
        return super().delete(request, *args, **kwargs)

# Admin view for ad management (Accessible by Superusers and Moderators)
class AdminAdListView(LoginRequiredMixin, UserPassesTestMixin, ListView): # Changed mixins
    """
    Displays a list of all ads for admin/moderator management.
    Allows filtering by status and bulk actions (restricted for moderators).
    Accessible by superusers and moderators.
    """
    model = Ad
    template_name = 'listings/admin/ad_list.html'
    context_object_name = 'ads'
    paginate_by = 20  # Show 20 ads per page

    def test_func(self):
        """Allow access if user is superuser or moderator."""
        # Assumes RoleMiddleware is active and adds is_moderator
        return self.request.user.is_superuser or getattr(self.request.user, 'is_moderator', False)

    def get_queryset(self):
        """
        Return ads filtered by status if specified in GET parameters.
        """
        queryset = Ad.objects.all().order_by('-created_at')
        status = self.request.GET.get('status')
        if status in [Ad.STATUS_PENDING, Ad.STATUS_APPROVED, Ad.STATUS_DENIED]:
            queryset = queryset.filter(status=status)
        return queryset

    def get_context_data(self, **kwargs):
        """
        Add status filter and status constants to context.
        """
        context = super().get_context_data(**kwargs)
        context['status_filter'] = self.request.GET.get('status', '')
        context['pending_count'] = Ad.objects.filter(status=Ad.STATUS_PENDING).count()
        # Add status constants to context for use in template links
        context['STATUS_PENDING'] = Ad.STATUS_PENDING
        context['STATUS_APPROVED'] = Ad.STATUS_APPROVED
        context['STATUS_DENIED'] = Ad.STATUS_DENIED
        return context

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests for bulk actions.
        """
        action = request.POST.get('action')
        selected_ids = request.POST.getlist('selected_ads')

        if action == 'approve_selected' and selected_ids:
            Ad.objects.filter(id__in=selected_ids).update(status=Ad.STATUS_APPROVED)
            messages.success(request, f"{len(selected_ids)} ad(s) approved successfully.")
        
        elif action == 'deny_selected' and selected_ids:
            Ad.objects.filter(id__in=selected_ids).update(status=Ad.STATUS_DENIED)
            messages.success(request, f"{len(selected_ids)} ad(s) denied successfully.")
        
        elif action == 'approve_all_pending':
            count = Ad.objects.filter(status=Ad.STATUS_PENDING).update(status=Ad.STATUS_APPROVED)
            messages.success(request, f"All {count} pending ad(s) approved successfully.")
        
        elif action == 'deny_all_pending':
            count = Ad.objects.filter(status=Ad.STATUS_PENDING).update(status=Ad.STATUS_DENIED)
            messages.success(request, f"All {count} pending ad(s) denied successfully.")

        return redirect('admin_ad_list')

# Ads Management main page (formerly Admin Tools)
class AdsManagementView(SuperuserRequiredMixin, TemplateView):
    """
    Main ads management page with links to various management sections.
    Only accessible by superusers.
    """
    template_name = 'listings/admin/tools.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pending_ads_count'] = Ad.objects.filter(status=Ad.STATUS_PENDING).count()
        context['categories_count'] = Category.objects.count()
        context['subcategories_count'] = SubCategory.objects.count()
        # Add pending flags count
        context['pending_flags_count'] = UserFlag.objects.filter(status=UserFlag.STATUS_PENDING).count()
        return context

# User dashboard view
class UserDashboardView(LoginRequiredMixin, ListView):
    """
    Displays a dashboard for logged-in users showing all their ads and their status.
    """
    model = Ad
    template_name = 'listings/user/dashboard.html'
    context_object_name = 'ads'
    
    def get_queryset(self):
        """Return only the current user's ads."""
        return Ad.objects.filter(author=self.request.user).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pending_count'] = self.get_queryset().filter(status=Ad.STATUS_PENDING).count()
        context['approved_count'] = self.get_queryset().filter(status=Ad.STATUS_APPROVED).count()
        context['denied_count'] = self.get_queryset().filter(status=Ad.STATUS_DENIED).count()
        return context

# Ad update view
class UpdateAdView(LoginRequiredMixin, UpdateView):
    """
    Allows users to edit their own ads.
    Edited ads are set back to 'pending' status for admin approval.
    """
    model = Ad
    form_class = AdForm
    template_name = 'listings/ad_form.html'
    success_url = reverse_lazy('user_dashboard')
    
    def get_queryset(self):
        """Ensure users can only edit their own ads."""
        return Ad.objects.filter(author=self.request.user)
    
    def form_valid(self, form):
        """Set status back to pending when an ad is edited."""
        form.instance.status = Ad.STATUS_PENDING
        messages.success(self.request, "Your ad has been updated and is pending admin approval.")
        return super().form_valid(form)

# Ad delete view
class DeleteAdView(LoginRequiredMixin, DeleteView):
    """
    Allows users to delete their own ads.
    Requires confirmation before deletion.
    """
    model = Ad
    template_name = 'listings/ad_confirm_delete.html' # Need to create this template
    success_url = reverse_lazy('user_dashboard')

    def get_queryset(self):
        """Ensure users can only delete their own ads."""
        return Ad.objects.filter(author=self.request.user)

    def delete(self, request, *args, **kwargs):
        """Add a success message upon deletion."""
        messages.success(request, "Your ad has been deleted successfully.")
        return super().delete(request, *args, **kwargs)

# Admin view for user management (ban/unban/moderator)
class UserManagementListView(SuperuserRequiredMixin, ListView):
    """
    Displays a list of users for admin management.
    Allows admins to ban/unban users and assign/remove moderator role.
    Only accessible by superusers.
    """
    model = User
    template_name = 'listings/admin/user_management_list.html'
    context_object_name = 'users'
    paginate_by = 20

    def get_queryset(self):
        """
        Order users by username and annotate with moderator status.
        """
        # Check if the Moderators group exists
        try:
            moderator_group = Group.objects.get(name='Moderators')
            # Annotate each user with a boolean indicating if they are in the Moderators group
            queryset = User.objects.annotate(
                is_moderator=Exists(moderator_group.user_set.filter(pk=OuterRef('pk')))
            ).order_by('username')
        except Group.DoesNotExist:
            # If group doesn't exist, annotate all as False
             messages.warning(self.request, "The 'Moderators' group does not exist. Please create it in the Django admin.")
             queryset = User.objects.annotate(is_moderator=Exists(User.objects.none())).order_by('username') # Annotate with always false

        return queryset

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to ban/unban users or change moderator status.
        """
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')

        if not user_id or not action:
             messages.error(request, "Invalid request.")
             return redirect('user_management_list')

        user_to_modify = get_object_or_404(User, pk=user_id)

        # Prevent admins from modifying themselves
        if user_to_modify == request.user:
            messages.error(request, "You cannot modify your own account status or roles here.")
            return redirect('user_management_list')

        # Prevent modifying other superusers (except self, handled above)
        if user_to_modify.is_superuser:
            messages.error(request, "Superuser accounts cannot be modified through this interface.")
            return redirect('user_management_list')

        # --- Handle Ban/Unban ---
        if action == 'ban':
            user_to_modify.is_active = False
            user_to_modify.save()
            messages.success(request, f"User '{user_to_modify.username}' has been banned (deactivated).")
        elif action == 'unban':
            user_to_modify.is_active = True
            user_to_modify.save()
            messages.success(request, f"User '{user_to_modify.username}' has been unbanned (activated).")

        # --- Handle Moderator Role ---
        elif action in ['make_moderator', 'remove_moderator']:
            try:
                moderator_group = Group.objects.get(name='Moderators')
                if action == 'make_moderator':
                    user_to_modify.groups.add(moderator_group)
                    messages.success(request, f"User '{user_to_modify.username}' has been added to the Moderators group.")
                elif action == 'remove_moderator':
                    user_to_modify.groups.remove(moderator_group)
                    messages.success(request, f"User '{user_to_modify.username}' has been removed from the Moderators group.")
            except Group.DoesNotExist:
                 messages.error(request, "Action failed: The 'Moderators' group does not exist.")

        else:
             messages.error(request, f"Unknown action: {action}")


        return redirect('user_management_list')


# Moderator view to flag a user
class FlagUserView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    Allows moderators to flag a specific user.
    """
    model = UserFlag
    form_class = UserFlagForm
    template_name = 'listings/flag_user_form.html' # Need to create this template
    # success_url = reverse_lazy('home') # Redirect somewhere appropriate after flagging

    def test_func(self):
        """Allow access only if user is a moderator."""
        # Assumes RoleMiddleware is active and adds is_moderator
        return getattr(self.request.user, 'is_moderator', False)

    def get_context_data(self, **kwargs):
        """Add the user being flagged to the context."""
        context = super().get_context_data(**kwargs)
        # Get the user being flagged from the URL kwargs
        context['flagged_user'] = get_object_or_404(User, pk=self.kwargs.get('user_id'))
        # Prevent flagging self
        if context['flagged_user'] == self.request.user:
             messages.error(self.request, "You cannot flag yourself.")
             # Redirect or raise PermissionDenied? Redirecting might be better UX.
             # For now, let the template handle this, but ideally redirect earlier.
             context['cannot_flag_self'] = True # Add flag for template
        # Prevent flagging superusers
        elif context['flagged_user'].is_superuser:
             messages.error(self.request, "Superusers cannot be flagged.")
             context['cannot_flag_superuser'] = True # Add flag for template

        return context

    def form_valid(self, form):
        """Set the moderator and flagged_user before saving."""
        flagged_user = get_object_or_404(User, pk=self.kwargs.get('user_id'))

        # Double-check permissions here in case context check fails or is bypassed
        if flagged_user == self.request.user:
             messages.error(self.request, "You cannot flag yourself.")
             return redirect('home') # Or wherever appropriate
        if flagged_user.is_superuser:
             messages.error(self.request, "Superusers cannot be flagged.")
             return redirect('home') # Or wherever appropriate

        form.instance.moderator = self.request.user
        form.instance.flagged_user = flagged_user
        messages.success(self.request, f"User '{flagged_user.username}' has been flagged for review.")
        # Determine success URL - maybe back to the ad detail? Or user dashboard?
        # For now, redirect home. Consider redirecting back to the referring page if possible.
        self.success_url = reverse_lazy('home')
        return super().form_valid(form)


# Admin view to review flagged users
class FlaggedUserListView(SuperuserRequiredMixin, ListView):
    """
    Displays a list of pending user flags for admin review.
    Allows admins to ban users based on flags.
    """
    model = UserFlag
    template_name = 'listings/admin/flagged_user_list.html' # Need to create this template
    context_object_name = 'flags'
    paginate_by = 20

    def get_queryset(self):
        """Return only pending flags, prefetch related users."""
        return UserFlag.objects.filter(status=UserFlag.STATUS_PENDING)\
               .select_related('flagged_user', 'moderator')\
               .order_by('-created_at')

    def post(self, request, *args, **kwargs):
        """Handle banning users based on selected flags."""
        action = request.POST.get('action')
        selected_flag_ids = request.POST.getlist('selected_flags')
        processed_count = 0
        banned_users = []

        flags_to_process = UserFlag.objects.none() # Start with empty queryset

        if action == 'ban_selected' and selected_flag_ids:
            flags_to_process = UserFlag.objects.filter(
                pk__in=selected_flag_ids,
                status=UserFlag.STATUS_PENDING
            ).select_related('flagged_user') # Select related user for efficiency
        elif action == 'ban_all_pending':
             flags_to_process = UserFlag.objects.filter(
                 status=UserFlag.STATUS_PENDING
             ).select_related('flagged_user')

        if not flags_to_process.exists():
             messages.warning(request, "No pending flags selected or found for the specified action.")
             return redirect('flagged_user_list')

        for flag in flags_to_process:
            user_to_ban = flag.flagged_user
            # Double-check we are not banning superusers or self (shouldn't happen if flagging logic is correct)
            if user_to_ban.is_superuser or user_to_ban == request.user:
                messages.error(request, f"Cannot ban superuser or yourself ({user_to_ban.username}). Skipping.")
                continue

            if user_to_ban.is_active:
                user_to_ban.is_active = False
                user_to_ban.save()
                banned_users.append(user_to_ban.username)
                processed_count += 1

            # Mark the flag as resolved regardless of whether user was already inactive
            flag.status = UserFlag.STATUS_RESOLVED
            flag.save()

        if processed_count > 0:
             messages.success(request, f"Successfully banned {processed_count} user(s): {', '.join(banned_users)}.")
        else:
             messages.info(request, "No users were banned (they might have been already inactive or were skipped). Flags have been marked as resolved.")


        return redirect('flagged_user_list') # Redirect back to the list


# API view to get subcategories for a given category
def get_subcategories(request, category_id):
    """
    Returns a JSON response containing subcategories for the given category_id.
    Used for dynamically populating the subcategory dropdown in the ad form.
    """
    try:
        # Ensure the category exists
        category = Category.objects.get(pk=category_id)
        subcategories = SubCategory.objects.filter(category=category).order_by('name')
        # Convert queryset to a list of dictionaries
        data = [{'id': sub.id, 'name': sub.name} for sub in subcategories]
        return JsonResponse(data, safe=False)
    except Category.DoesNotExist:
        # Return an empty list if the category doesn't exist
        return JsonResponse([], safe=False)
    except Exception as e:
        # Handle potential errors, log them if necessary
        # logger.error(f"Error fetching subcategories: {e}") # Example logging
        return JsonResponse({'error': 'An error occurred'}, status=500)
