from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, help_text="E.g., 'women', 'men', 'kids'")
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

class Product(models.Model):
    AVAILABILITY_CHOICES = [
        ('in_stock', 'In Stock (Ready to deliver now)'),
        ('available_to_order', 'Available to Order (I will fetch it)'),
        ('out_of_stock', 'Out of Stock (Unavailable)'),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Regular price in UGX")
    promotional_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Sale price in UGX (Leave blank if no sale)")
    
    sizes_available = models.CharField(max_length=100, help_text="E.g., '38, 39, 40, 41'")
    colors_available = models.CharField(max_length=100, help_text="E.g., 'Red, Black, Blue'")

    main_image = models.ImageField(upload_to='products/', blank=True, null=True, help_text="The primary display image")
    availability_status = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='in_stock')
    is_featured = models.BooleanField(default=False, help_text="Show this on the Homepage?")
    views = models.PositiveIntegerField(default=0, help_text="Tracks popularity for sorting")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product (Shoe)"
        verbose_name_plural = "Products (Shoes)"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.get_availability_status_display()}"

    def get_display_price(self):
        if self.promotional_price:
            return self.promotional_price
        return self.price

# NEW MODEL: Multiple angle images
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_angles/', help_text="Extra angle/detail shots")
    alt_text = models.CharField(max_length=100, blank=True, help_text="E.g., 'Side view'")
    
    class Meta:
        verbose_name = "Product Angle Image"
        ordering = ['id']

    def __str__(self):
        return f"Angle image for {self.product.name}"

# RESTORED MODEL: Customer Reviews
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], help_text="1 to 5 Stars")
    comment = models.TextField()
    customer_name = models.CharField(max_length=100)
    is_approved = models.BooleanField(default=False, help_text="Justin must approve reviews before they show on site")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Product Review"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.rating}-Star Review by {self.customer_name}"
