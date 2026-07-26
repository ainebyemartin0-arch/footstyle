from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import SiteSettings, LocationBanner

# BRANDING THE ADMIN DASHBOARD
admin.site.site_header = "FootStyle Administration"
admin.site.site_title = "FootStyle Admin Portal"
admin.site.index_title = "Welcome to the Boss Lady Control Room"

class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'slogan', 'currency', 'whatsapp_number')
    def has_add_permission(self, request):
        if SiteSettings.objects.exists():
            return False
        return super().has_add_permission(request)

class LocationBannerAdmin(admin.ModelAdmin):
    list_display = ('message', 'is_active', 'updated_at')

class CustomerProfileInline(admin.StackedInline):
    model = User.profile
    can_delete = False
    verbose_name = "Customer Details (Phone & Address)"
    verbose_name_plural = "Customer Details"

class CustomUserAdmin(UserAdmin):
    inlines = (CustomerProfileInline,)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(SiteSettings, SiteSettingsAdmin)
admin.site.register(LocationBanner, LocationBannerAdmin)
