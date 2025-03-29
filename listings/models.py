from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=110, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories" # Correct pluralization in admin

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # Useful for admin site or linking directly
        return reverse('category_detail', kwargs={'slug': self.slug}) # Placeholder name

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=110, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Subcategories"
        unique_together = ('category', 'name') # Ensure unique subcategory names within a category

    def save(self, *args, **kwargs):
        if not self.slug:
            # Combine category slug and subcategory name for uniqueness if needed
            self.slug = slugify(f"{self.category.name}-{self.name}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category.name} > {self.name}"

    def get_absolute_url(self):
        return reverse('subcategory_detail', kwargs={'slug': self.slug}) # Placeholder name

class Ad(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_DENIED = 'denied'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending Approval'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_DENIED, 'Denied'),
    ]

    PRICE_TYPE_FIXED = 'fixed'
    PRICE_TYPE_PER_HOUR = 'per_hour'
    PRICE_TYPE_NEGOTIABLE = 'negotiable'
    PRICE_TYPE_FREE = 'free' # Added Free as an option
    PRICE_TYPE_CHOICES = [
        (PRICE_TYPE_FIXED, 'Fixed Price'),
        (PRICE_TYPE_PER_HOUR, 'Per Hour'),
        (PRICE_TYPE_NEGOTIABLE, 'Negotiable'),
        (PRICE_TYPE_FREE, 'Free'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    price_type = models.CharField(
        max_length=10,
        choices=PRICE_TYPE_CHOICES,
        default=PRICE_TYPE_FIXED
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) # Keep allowing null
    location = models.CharField(max_length=150, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='ads')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, related_name='ads')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ads')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # image = models.ImageField(upload_to='ad_images/', blank=True, null=True) # Requires Pillow

    class Meta:
        ordering = ['-created_at'] # Show newest ads first by default

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # Assumes you'll have a URL named 'ad_detail' that takes the ad's pk
        return reverse('ad_detail', kwargs={'pk': self.pk})


class UserFlag(models.Model):
   """Model to store flags submitted by moderators against users."""
   REASON_SPAM = 'SPAM'
   REASON_SCAM = 'SCAM'
   REASON_HACK = 'HACK'
   REASON_OTHER = 'OTHER'
   REASON_CHOICES = [
       (REASON_SPAM, 'Spamming'),
       (REASON_SCAM, 'Scamming / Fraud'),
       (REASON_HACK, 'Hacking / Malicious Activity'),
       (REASON_OTHER, 'Other (See Details)'),
   ]

   STATUS_PENDING = 'PENDING'
   STATUS_RESOLVED = 'RESOLVED'
   STATUS_CHOICES = [
       (STATUS_PENDING, 'Pending Review'),
       (STATUS_RESOLVED, 'Resolved'),
   ]

   flagged_user = models.ForeignKey(
       User,
       on_delete=models.CASCADE,
       related_name='flags_received',
       help_text="The user being reported."
   )
   moderator = models.ForeignKey(
       User,
       on_delete=models.SET_NULL, # Keep flag even if moderator account deleted
       null=True,
       related_name='flags_submitted',
       help_text="The moderator who submitted this flag."
   )
   reason = models.CharField(
       max_length=10,
       choices=REASON_CHOICES,
       help_text="The primary reason for flagging this user."
   )
   details = models.TextField(
       blank=True,
       help_text="Provide specific details, especially if 'Other' reason is selected."
   )
   created_at = models.DateTimeField(auto_now_add=True)
   status = models.CharField(
       max_length=10,
       choices=STATUS_CHOICES,
       default=STATUS_PENDING,
       db_index=True # Index for faster filtering
   )

   class Meta:
       ordering = ['-created_at'] # Show newest flags first
       verbose_name = "User Flag"
       verbose_name_plural = "User Flags"

   def __str__(self):
       return f"Flag for {self.flagged_user.username} by {self.moderator.username if self.moderator else 'Deleted Moderator'} ({self.get_reason_display()})"
