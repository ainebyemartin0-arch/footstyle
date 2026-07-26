from django.db import models
from django.core.exceptions import ValidationError

# SINGLETON MODEL: Ensures Justin can only create ONE SiteSettings object
class SiteSettings(models.Model):
    site_name = models.CharField(max_length=50, default="FootStyle")
    slogan = models.CharField(max_length=100, default="Fashion Starts from the Ground Up.")
    logo = models.ImageField(upload_to='site/', blank=True, null=True)
    currency = models.CharField(max_length=3, default="UGX")
    default_delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=5000.00)
    whatsapp_number = models.CharField(max_length=15, default="2567XXXXXXXX")

    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.site_name

    # Enforce Singleton: Prevent adding more than one setting
    def clean(self):
        if SiteSettings.objects.exclude(id=self.id).exists():
            raise ValidationError("You can only create one Site Settings entry. Edit the existing one instead.")


# DAILY LOCATION BANNER: Justin's "No Shop" Killer Feature
class LocationBanner(models.Model):
    message = models.CharField(max_length=200, help_text="E.g., 'Today I am near Kampala Road / Nakasero'")
    is_active = models.BooleanField(default=True, help_text="Check this to show the banner to customers on the website")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Daily Location Banner"
        verbose_name_plural = "Daily Location Banner"

    def __str__(self):
        return self.message if self.is_active else f"[DISABLED] {self.message}"


# NOTIFICATIONS: System alerts for Justin
class Notification(models.Model):
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.message
