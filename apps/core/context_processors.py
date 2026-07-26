from .models import SiteSettings, LocationBanner

def global_settings(request):
    try:
        settings = SiteSettings.objects.first()
    except SiteSettings.DoesNotExist:
        settings = None

    try:
        location = LocationBanner.objects.filter(is_active=True).first()
    except LocationBanner.DoesNotExist:
        location = None

    return {
        'site_settings': settings,
        'location_banner': location
    }
