from django.contrib import admin
from django.urls import path, include
from .views import home_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page),  # Root endpoint
    path('home/', home_page),  # Home page endpoint
    path('api/', include('api.urls')),  # Include API routes
    path('auth/', include('rest_framework.urls')),  # Optional: Default DRF login/logout
]
