from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Ad, Category, SubCategory

class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = [
            'title',
            'description',
            'price_type', # Add price_type
            'price',
            'location',
            'category',
            'subcategory',
            # 'image',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'price_type': forms.RadioSelect, # Use radio buttons for price type
        }
        labels = {
            'price_type': 'Pricing', # Nicer label
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap 'form-control' class to most fields
        for field_name, field in self.fields.items():
            widget = field.widget
            # Apply 'form-control' to text, number, textarea, etc.
            if isinstance(widget, (forms.TextInput, forms.NumberInput, forms.EmailInput, forms.PasswordInput, forms.URLInput, forms.DateInput, forms.DateTimeInput, forms.TimeInput, forms.Textarea)):
                widget.attrs.update({'class': 'form-control'})
            # Apply 'form-select' to Select widgets
            elif isinstance(widget, forms.Select):
                 widget.attrs.update({'class': 'form-select'})
            # RadioSelect and CheckboxSelectMultiple need special handling (usually done in template)
            # CheckboxInput might need 'form-check-input' (also usually in template)

        # --- Existing subcategory logic ---
        self.fields['subcategory'].queryset = SubCategory.objects.none()
        if not self.initial.get('category') and not (self.data and self.data.get('category')):
            self.fields['subcategory'].required = False
        elif self.instance.pk and self.instance.category:
            self.fields['subcategory'].queryset = self.instance.category.subcategories.order_by('name')
        elif self.data and self.data.get('category'):
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = SubCategory.objects.filter(category_id=category_id).order_by('name')
            except (ValueError, TypeError):
                pass

        # --- Price field logic ---
        # Price is not required by default, validation handled in clean()
        self.fields['price'].required = False


    def clean(self):
        cleaned_data = super().clean()
        price_type = cleaned_data.get('price_type')
        price = cleaned_data.get('price')

        # Price is required and must be positive for Fixed or Per Hour
        if price_type in [Ad.PRICE_TYPE_FIXED, Ad.PRICE_TYPE_PER_HOUR]:
            if price is None:
                self.add_error('price', 'Price is required for this pricing type.')
            elif price <= 0:
                 self.add_error('price', 'Price must be a positive number.')
        # Price should be ignored (set to None) for Negotiable or Free
        elif price_type in [Ad.PRICE_TYPE_NEGOTIABLE, Ad.PRICE_TYPE_FREE]:
            cleaned_data['price'] = None # Ensure price is saved as NULL

        return cleaned_data

class CategoryForm(forms.ModelForm):
    """Form for creating and updating categories."""
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class SubCategoryForm(forms.ModelForm):
    """Form for creating and updating subcategories."""
    class Meta:
        model = SubCategory
        fields = ['category', 'name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class CustomUserCreationForm(UserCreationForm):
    """
    Custom user creation form with Bootstrap styling and simplified password validation.
    """
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'
            
        # Remove password validation help texts and constraints for this proof of concept
        self.fields['password1'].help_text = 'Enter any password.'
        self.fields['password1'].validators = []
        self.fields['password2'].help_text = 'Enter the same password as before, for verification.'
            
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
        
    # Override the clean_password2 method to remove password validation
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        return password2


# Import UserFlag model
from .models import UserFlag

class UserFlagForm(forms.ModelForm):
   """Form for moderators to flag users."""
   class Meta:
       model = UserFlag
       fields = ['reason', 'details']
       widgets = {
           'reason': forms.RadioSelect, # Use radio buttons for reason
           'details': forms.Textarea(attrs={'rows': 3}),
       }
       labels = {
           'details': 'Details (Required if reason is Other)',
       }

   def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       # Apply Bootstrap classes
       self.fields['details'].widget.attrs.update({'class': 'form-control'})
       # RadioSelect needs styling in the template (e.g., using form-check)

   def clean(self):
       cleaned_data = super().clean()
       reason = cleaned_data.get('reason')
       details = cleaned_data.get('details')

       # Require details if 'Other' reason is selected
       if reason == UserFlag.REASON_OTHER and not details:
           self.add_error('details', 'Please provide details when selecting "Other".')

       return cleaned_data