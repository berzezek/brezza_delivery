from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('grappelli/', include('grappelli.urls')), # grappelli URLS

    path('api/v1/', include(('delivery.api.urls', 'delivery'), namespace='delivery')),
    path('', include('delivery.urls')),
]
