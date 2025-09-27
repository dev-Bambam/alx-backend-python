from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet

# Setup the DRF Router for top-level resources (Conversations)
# FIXED: Changed SimpleRouter to DefaultRouter to satisfy test requirement
router = DefaultRouter()
router.register(r'chats', ConversationViewSet, basename='chat')

# Define nested message paths manually, as DRF Router does not handle nesting
urlpatterns = [
    # 1. URL for listing messages in a specific chat (GET) and sending a new message (POST)
    # The <int:chat_pk> captures the ID of the parent conversation.
    path(
        'chats/<uuid:chat_pk>/messages/', 
        MessageViewSet.as_view({'get': 'list', 'post': 'create'}), 
        name='chat-messages-list'
    ),

    # 2. URL for retrieving, updating, or deleting a specific message (GET, PUT, DELETE)
    path(
        'chats/<uuid:chat_pk>/messages/<uuid:pk>/', 
        MessageViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), 
        name='chat-messages-detail'
    ),
]

# Append the router URLs (for /chats/ and /chats/{pk}/) to the list
urlpatterns += router.urls
