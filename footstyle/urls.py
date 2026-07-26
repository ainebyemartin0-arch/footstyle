from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('', include('apps.catalog.urls')),
    path('', include('apps.orders.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom Error Handlers (Points to our Elite UI 404/500 templates)
handler404 = 'apps.core.views.custom_404'
handler500 = 'apps.core.views.custom_500'
