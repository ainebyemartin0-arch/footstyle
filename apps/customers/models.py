from django.db import models
from django.contrib.auth.models import User

class CustomerProfile(models.Model):
    """
    Extends the default Django User to include Justin's specific needs:
    Phone numbers and default delivery addresses for faster checkouts.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, help_text="Primary contact number (E.g., 0771234567)")
    
    # Default delivery info (So customers don't have to type it every time they buy shoes)
    default_address = models.CharField(max_length=255, blank=True, null=True, help_text="E.g., 'Nakasero, near the market'")
    default_landmark = models.CharField(max_length=100, blank=True, null=True, help_text="E.g., 'Next to the red building'")
    
    # Justin's Business Logic: She can block problematic customers
    is_active = models.BooleanField(default=True, help_text="If a customer is troublesome, uncheck this to block them from ordering")
    
    # Internal notes for Justin
    admin_notes = models.TextField(blank=True, null=True, help_text="Internal notes about this customer (E.g., 'Always pays late', 'VIP customer')")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Customer Profile"
        verbose_name_plural = "Customer Profiles"

    def __str__(self):
        return f"{self.user.username} - {self.phone_number}"
