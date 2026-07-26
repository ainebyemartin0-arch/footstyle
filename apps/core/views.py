from django.shortcuts import render
from apps.catalog.models import Product, Category # FIXED: Removed SiteSettings import

def home_view(request):
    featured_products = Product.objects.filter(is_featured=True, availability_status__in=['in_stock', 'available_to_order'])[:4]
    categories = Category.objects.all()
    context = { 'featured_products': featured_products, 'categories': categories }
    return render(request, 'index.html', context)

def about_view(request):
    return render(request, 'about.html')

def contact_view(request):
    return render(request, 'contact.html')

def terms_view(request):
    return render(request, 'terms.html')

def faq_view(request):
    return render(request, 'faq.html')

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def custom_500(request):
    return render(request, '500.html', status=500)
