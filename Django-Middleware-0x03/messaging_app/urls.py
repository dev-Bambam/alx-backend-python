from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT Authentication Endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # DRF Login/Logout for Browsable API (Resolves 'api-auth' check)
    path('api-auth/', include('rest_framework.urls')),

    # API Endpoints (delegated to the chats app)
    # This path is what creates the required '/api/' prefix.
    # The include() function delegates all the routes defined in chats/urls.py
    path('api/', include('chats.urls')),
]
