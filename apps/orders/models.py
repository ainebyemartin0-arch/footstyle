from decimal import Decimal
from django.db import models
from apps.catalog.models import Product

class Order(models.Model):
    PAYMENT_CHOICES = [
        ('momo', 'MTN Mobile Money (MoMo)'),
        ('airtel', 'Airtel Money'),
        ('cash', 'Cash on Delivery'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    customer_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length=255)
    landmark = models.CharField(max_length=100, blank=True, null=True)
    
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cash')
    notes = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Customer Order"
        verbose_name_plural = "Customer Orders"
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.id} - {self.customer_name} ({self.get_status_display()})"

    # Smart Auto-Calculation: Safely convert to Decimal before adding!
    def save(self, *args, **kwargs):
        # Convert both to Decimal strings to avoid 'Decimal + Float' TypeError
        sub = Decimal(str(self.subtotal))
        fee = Decimal(str(self.delivery_fee))
        self.total = sub + fee
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


class OrderStatusLog(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='status_logs')
    status = models.CharField(max_length=20, choices=Order.STATUS_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Status Log"
        ordering = ['timestamp']

    def __str__(self):
        return f"Order {self.order.id} changed to {self.get_status_display()}"
