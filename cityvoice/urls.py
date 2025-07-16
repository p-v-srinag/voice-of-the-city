# cityvoice/urls.py

from django.contrib import admin
from django.urls import path, include

# ✅ For serving static files (e.g. MP3 output)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # ✅ Include core app routes
]

# ✅ Serve static files during development
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
