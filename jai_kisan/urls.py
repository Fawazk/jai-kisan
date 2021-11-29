
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('adminpanel/',include('admin_panel.urls')),
    path('store/',include('store.urls')),
    path('cart/',include('cart.urls')),
    path('orders/',include('orders.urls')),
    path('offer/',include('offer.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
