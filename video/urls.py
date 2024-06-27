
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('app.dashboard.urls')),
    path('client/', include('app.client.urls')),
    path('account/', include('app.account.urls')),
]
