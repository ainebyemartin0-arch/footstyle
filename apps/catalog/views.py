from django.shortcuts import render, get_object_or_404
from .models import Category, Product, ProductImage
from django.views.decorators.http import require_POST

def product_list_view(request, category_slug=None):
    categories = Category.objects.all()
    products = Product.objects.filter(availability_status__in=['in_stock', 'available_to_order'])
    
    selected_category = None
    sort_by = request.GET.get('sort', '-created_at')
    search_query = request.GET.get('search', '')

    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)

    if search_query:
        products = products.filter(name__icontains=search_query)

    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'popularity':
        products = products.order_by('-views')
    else:
        products = products.order_by('-created_at')

    context = {
        'categories': categories,
        'products': products,
        'selected_category': selected_category,
        'sort_by': sort_by,
        'search_query': search_query,
    }
    return render(request, 'catalog.html', context)


def product_detail_view(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    product.views += 1
    product.save(update_fields=['views'])

    size_list = [s.strip() for s in product.sizes_available.split(',')] if product.sizes_available else []
    color_list = [c.strip() for c in product.colors_available.split(',')] if product.colors_available else []
    
    # FETCH EXTRA ANGLE IMAGES
    angle_images = ProductImage.objects.filter(product=product)

    whatsapp_base = f"https://wa.me/256761237882?text="
    default_msg = f"Hi Justin! I'm interested in the {product.name} (UGX {product.get_display_price()}). Is it available?"
    whatsapp_link = whatsapp_base + default_msg.replace(' ', '%20')

    context = {
        'product': product,
        'whatsapp_link': whatsapp_link,
        'size_list': size_list,
        'color_list': color_list,
        'angle_images': angle_images, # Pass to template
    }
    return render(request, 'product_detail.html', context)
