from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Chat, Message
from .permissions import isParticipantOfConversation
from .serializers import ChatSerializer, MessageSerializer

class ChatViewSet(viewsets.ModelViewSet):
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated, isParticipantOfConversation]

    def get_queryset(self):
        return Chat.objects.filter(user=self.request.user).order_by('-created_at')
    
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
    

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, isParticipantOfConversation]

    def get_queryset(self):
        return Message.objects.filter(chat__user=self.request.user).order_by('timestamp')
    
    def perform_create(self, serializer):
        chat_id = self.kwargs.get('chat_pk')
        chat = Chat.objects.get(pk=chat_id)
        if chat.user != self.request.user:
            raise PermissionDenied('You can only send messages to your own chats')
        serializer.save(sender=self.request.user, chat=chat)