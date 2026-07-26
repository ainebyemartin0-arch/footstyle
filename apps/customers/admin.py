from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import CustomerProfile

# Define an inline admin descriptor for CustomerProfile
# This puts the Phone/Address INSIDE the standard User page, so Justin doesn't have to click two separate menus!
class CustomerProfileInline(admin.StackedInline):
    model = CustomerProfile
    can_delete = False
    verbose_name = "Customer Details (Phone & Address)"
    verbose_name_plural = "Customer Details"

# Extend the existing Django UserAdmin to include our CustomerProfileInline
class CustomUserAdmin(UserAdmin):
    inlines = (CustomerProfileInline,)

# Re-register User with our customized admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
