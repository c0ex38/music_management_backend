# music_management_backend/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin paneline erişim
    path('api/', include('music.urls')),  # Müzik API rotasına yönlendirme
]

# Müzik dosyalarına yerel erişim için ayar
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Medya dosyalarının erişimi
