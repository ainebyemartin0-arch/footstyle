from django.contrib import admin
from .models import Order, OrderItem, OrderStatusLog

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1 
    # REMOVED readonly_fields so the price can be typed in and saved without error!

class OrderStatusLogInline(admin.TabularInline):
    model = OrderStatusLog
    extra = 0
    readonly_fields = ('status', 'timestamp')
    can_delete = False 

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'phone_number', 'subtotal', 'delivery_fee', 'total', 'status', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('customer_name', 'phone_number', 'id')
    list_editable = ('status',) 
    
    # Justin can manually edit subtotal and delivery_fee. 
    # 'total' is readonly because the model calculates it automatically!
    readonly_fields = ('total', 'created_at', 'updated_at')
    
    inlines = [OrderItemInline, OrderStatusLogInline]

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(OrderStatusLog)
