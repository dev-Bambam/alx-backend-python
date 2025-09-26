from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView
)

from chats.views import ChatViewSet, MessageViewSet

router = SimpleRouter()
# The router will automatically generate all CRUD URLs for the ChatViewSet
router.register(r'chats', ChatViewSet, basename='chat')

urlpatterns = [
    # --- JWT Authentication Paths --- 
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # --- DRF Router Paths for (ChatViewSet) --- 
    # This includes paths like /api/chats and /api/chats/{pk}
    path('api/', include(router.urls)),

    # --- Nested Messages Paths (for MessageViewSet) ---
    
    # Path for LISTING all messages in a chat and CREATING a new message (POST).
    # This path is essential because it passes the 'chat_pk' argument to MessageViewSet.
    path(
        'api/chats/<int:chat_pk>/messages/',
        MessageViewSet.as_view({'get': 'list', 'post': 'create'}),
        name = 'chat-messages-list'
    ),

    # Path for RETRIEVING, UPDATING, or DELETING a specific message.
    # Requires both 'chat_pk' (parent) and 'pk' (message ID).
    path(
        'api/chats/<int:chat_pk>/messages/<int:pk>/',
        MessageViewSet.as_view({'get':'retrieve', 'put':'update', 'patch':'partial_update', 'delete':'destroy'}),
        name='chat-messages-details'
    )
]
