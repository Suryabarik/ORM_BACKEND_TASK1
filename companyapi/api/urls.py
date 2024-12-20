from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.authtoken.views import obtain_auth_token  # Add this import
from api.views import PatientViewSet, PrescriptionViewSet
from . import views

# Create the router and register the viewsets
router = routers.DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'prescriptions', PrescriptionViewSet, basename='prescription')

urlpatterns = [
    path('', include(router.urls)),  # Include all router endpoints under /
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Obtain JWT
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh JWT
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),  # Token Authentication (DRF token system)
    path('register/', views.register_user, name='register_user')
]
