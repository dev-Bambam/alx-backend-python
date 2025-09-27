# Suggested fix for chats/urls.py (Please apply this manually)

from django.urls import path, include
# You must import the router from the installed nested routers package
from rest_framework_nested import routers 
from .views import ConversationViewSet, MessageViewSet

# 1. Use DefaultRouter for the primary resource
router = routers.DefaultRouter()
router.register(r'chats', ConversationViewSet, basename='chat')

# 2. Use NestedDefaultRouter to define the nested resource
# The parent lookup value is 'chat_pk' which matches the view's kwargs
chats_router = routers.NestedDefaultRouter(router, r'chats', lookup='chat') 

# Register the nested messages endpoint
chats_router.register(r'messages', MessageViewSet, basename='chat-messages') 

# Combine all URLs
urlpatterns = [
    # Include the router URLs
    path('', include(router.urls)), 
    # Include the nested router URLs
    path('', include(chats_router.urls)),
]

