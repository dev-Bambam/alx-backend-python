from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from serializers import ChatSerializer, MessageSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .models import Chat, Message
from .permissions import isParticipantOfConversation
from pagination import StandardResultsSetPagination
from filters import MessageFilter

class ChatViewSet(viewsets.ModelViewSet):
    serializer_class = ChatSerializer
    permission_classes = [isParticipantOfConversation]

    def get_queryset(self):
        """Filters the queryset to filter chat where requesting user is participants of chat"""
        user = self.request.user
        return Chat.objects.filter(Q(participants=user)).order_by("-created_at")

    def perform_create(self, serializer):
        '''Automatically adds the authenticated user as a participant a when creating a new chat'''
        chat = serializer.save()
        chat.participants.add(self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [isParticipantOfConversation]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(Q(chat__participants = user)).order_by('timestamp')
    
    def perform_create(self, serializer):
        '''Automatically links the new message to the correct chat and sender'''
        conversation_id = self.kwargs.get('chat_pk')

        try:
            chat = Chat.objects.get(pk=conversation_id)
        except Chat.DoesNotExist:
            return Response(
                {'detail': 'conversation not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # check if user is a participant of the chat
        if self.request.user not in chat.participants.all():
            return Response(
                {'detail':'user not a participant'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer.save(sender=self.request.user, chat=chat)
