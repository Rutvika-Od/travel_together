from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rides import views as ride_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ride_views.home, name='home'),
    path('dashboard/', ride_views.dashboard, name='dashboard'),
    path('accounts/', include('accounts.urls')),
    path('drivers/', include('drivers.urls')),
    path('rides/', include('rides.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
