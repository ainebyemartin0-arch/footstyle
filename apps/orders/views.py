# -*- coding: utf-8 -*-
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from apps.catalog.models import Product
from apps.core.models import SiteSettings
from .models import Order, OrderItem

def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    subtotal = Decimal('0.00')

    for product_id, item_data in cart.items():
        product = Product.objects.get(id=product_id)
        quantity = item_data.get('quantity', 1)
        total_item_price = Decimal(str(product.get_display_price())) * quantity
        subtotal += total_item_price
        cart_items.append({ 'product': product, 'quantity': quantity, 'total_item_price': total_item_price })

    context = { 'cart_items': cart_items, 'subtotal': subtotal }
    return render(request, 'cart.html', context)

@require_POST
def add_to_cart_view(request, product_id):
    cart = request.session.get('cart', {})
    product = get_object_or_404(Product, id=product_id)
    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1
    else:
        cart[str(product_id)] = {'quantity': 1}
    request.session['cart'] = cart
    return redirect('cart')

@require_POST
def remove_from_cart_view(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    return redirect('cart')

def checkout_view(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('product_list')

    cart_items = []
    subtotal = Decimal('0.00')
    for product_id, item_data in cart.items():
        product = Product.objects.get(id=product_id)
        quantity = item_data.get('quantity', 1)
        total_item_price = Decimal(str(product.get_display_price())) * quantity
        subtotal += total_item_price
        cart_items.append({'product': product, 'quantity': quantity, 'total_item_price': total_item_price})

    if request.method == 'POST':
        order = Order.objects.create(
            customer_name=request.POST.get('customer_name'),
            phone_number=request.POST.get('phone_number'),
            address=request.POST.get('address'),
            landmark=request.POST.get('landmark', ''),
            payment_method=request.POST.get('payment_method', 'cash'),
            subtotal=subtotal,
            delivery_fee=Decimal('0.00'),
            total=subtotal,
            status='pending'
        )
        for item in cart_items:
            OrderItem.objects.create(order=order, product=item['product'], quantity=item['quantity'], price=item['product'].get_display_price())

        # DYNAMIC WHATSAPP: Pull number from SiteSettings DB
        settings = SiteSettings.objects.first()
        wa_number = settings.whatsapp_number if settings else '256761237882'
        whatsapp_base = f"https://wa.me/{wa_number}?text="
        
        msg_lines = [
            f"*NEW FOOTSTYLE ORDER (ID: {order.id})*",
            f"Name: {order.customer_name}",
            f"Phone: {order.phone_number}",
            f"Address: {order.address} ({order.landmark})",
            f"Payment: {order.get_payment_method_display()}",
            "-------------------",
        ]
        for item in cart_items:
            msg_lines.append(f"{item['product'].name} x {item['quantity']} = UGX {item['total_item_price']:,.0f}")
        msg_lines.append("-------------------")
        msg_lines.append(f"*Subtotal:* UGX {subtotal:,.0f}")
        msg_lines.append("(Delivery fee to be confirmed by Justin)")

        final_msg = "\n".join(msg_lines)
        whatsapp_link = whatsapp_base + final_msg.replace(' ', '%20').replace('\n', '%0A')

        request.session['cart'] = {}
        return redirect(whatsapp_link)

    context = { 'cart_items': cart_items, 'subtotal': subtotal }
    return render(request, 'checkout.html', context)
