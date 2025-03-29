from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group # Import Group
from .models import Category, SubCategory, Ad, UserFlag # Import UserFlag

# Register Category model
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

# Register SubCategory model
@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'slug')
    list_filter = ('category',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'category__name')

# Register Ad model
@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'subcategory', 'author', 'status', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'description', 'author__username')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('status',)
    date_hierarchy = 'created_at'
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'price', 'location')
        }),
        ('Classification', {
            'fields': ('category', 'subcategory')
        }),
        ('Status', {
            'fields': ('status', 'author', 'created_at', 'updated_at')
        }),
    )

# Register UserFlag model
@admin.register(UserFlag)
class UserFlagAdmin(admin.ModelAdmin):
   list_display = ('flagged_user', 'moderator', 'reason', 'status', 'created_at')
   list_filter = ('status', 'reason', 'created_at')
   search_fields = ('flagged_user__username', 'moderator__username', 'details')
   readonly_fields = ('created_at',)
   list_editable = ('status',) # Allow changing status directly in the list

# Customize User Admin
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    # 'is_active' is already included in the default fieldsets, no need to add it again.

# Unregister the default User admin
admin.site.unregister(User)
# Register the custom User admin
admin.site.register(User, UserAdmin)

# Register Group model (if not already registered by default auth app)
# Check if Group is already registered to avoid errors
if not admin.site.is_registered(Group):
     admin.site.register(Group)
