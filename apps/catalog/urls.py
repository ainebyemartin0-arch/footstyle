from django.urls import path
from .views import product_list_view, product_detail_view

urlpatterns = [
    path('catalog/', product_list_view, name='product_list'),
    path('catalog/<slug:category_slug>/', product_list_view, name='product_list_by_category'),
    path('product/<slug:product_slug>/', product_detail_view, name='product_detail'),
]
