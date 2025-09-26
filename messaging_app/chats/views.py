from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status
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
        conversation_id = self.kwargs.get('chat_pk')
        try:
            chat = Chat.objects.get(pk=conversation_id)
        except Chat.DoesNotExist:
            return Response(
                {'detail': 'conversation not found'},
                status=status.HTTP_404_NOT_FOUND 
            )
        
        if chat.user != self.request.user:
            return Response(
                {'detail': 'You do not have permission to perform this action'},
                status= status.HTTP_403_FORBIDDEN
            )
        
        serializer.save(sender = self.request.user, chat = chat)