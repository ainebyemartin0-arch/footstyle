from django.contrib import admin
from .models import Category, Product, Review, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    verbose_name = "Extra Angle Image"
    verbose_name_plural = "Upload Extra Angle Images"

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'promotional_price', 'availability_status', 'is_featured', 'views')
    list_filter = ('category', 'availability_status', 'is_featured')
    search_fields = ('name', 'description')
    list_editable = ('availability_status', 'is_featured')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'customer_name', 'rating', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'rating')
    list_editable = ('is_approved',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
