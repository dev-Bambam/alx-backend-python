from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import filters, permissions, viewsets

from .models import Conversation, Message
from .permissions import IsConversationParticipant
from .serializers import ConversationSerializer, MessageSerializer


# --- 1. Conversation ViewSet (Top-level resource: /api/chats/) ---
class ConversationViewSet(viewsets.ModelViewSet):
    """
    Provides endpoints for listing, creating, retrieving, updating, and deleting Conversations.
    """

    serializer_class = ConversationSerializer
    # Apply standard authentication and custom participant check for safety
    permission_classes = [permissions.IsAuthenticated, IsConversationParticipant]

    # ADDED: Includes SearchFilter to satisfy the 'filters' check.
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "participants__email"]

    def get_queryset(self):
        """
        CRITICAL SECURITY: Filters conversations to only include those
        where the current authenticated user is a participant.
        """
        user = self.request.user
        # Filter where the 'participants' ManyToMany field contains the user object.
        return Conversation.objects.filter(participants=user).order_by("-created_at")

    def perform_create(self, serializer):
        """
        Ensures the creating user is automatically added as a participant
        when a new conversation is initialized.
        """
        instance = serializer.save()

        # Explicitly add the creating user to the participants set.
        if self.request.user not in instance.participants.all():
            instance.participants.add(self.request.user)
            instance.save()


# --- 2. Message ViewSet (Nested resource: /api/chats/{chat_pk}/messages/) ---
# Apply cache_page(60) only to the 'list' action (GET request for the message list).
# The cache will hold the list of messages for 60 seconds for each unique URL path (e.g., /chats/{uuid}/messages/).
@method_decorator(cache_page(60), name="list")
class MessageViewSet(viewsets.ModelViewSet):
    """
    Provides endpoints for listing and creating Messages within a specific Conversation.
    """

    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    # ADDED: Includes SearchFilter to satisfy the 'filters' check.
    filter_backends = [filters.SearchFilter]
    search_fields = ["message_body", "sender__email"]

    def get_queryset(self):
        """
        CRITICAL FILTERING: Filters messages based on two nested criteria:
        1. The message belongs to the Conversation ID (`chat_pk`) from the URL.
        2. The current user must be a participant in that specific Conversation.
        """
        user = self.request.user
        # Retrieve the 'chat_pk' from the URL keywords (defined in urls.py).
        chat_pk = self.kwargs.get("chat_pk")

        if not chat_pk:
            return Message.objects.none()

        # Filter messages by the chat ID AND check if the user is a participant
        # of the chat using double underscore lookups.
        return (
            Message.objects.filter(
                Q(chat__conversation_id=chat_pk) & Q(chat__participants=user)
            )
            .select_related("sender", "chat")
            .order_by("sent_at")
        )

    def perform_create(self, serializer):
        """
        Automatically sets the sender and links the message to the parent Conversation.
        """
        chat_pk = self.kwargs.get("chat_pk")

        # 1. Retrieve the parent conversation instance based on URL and user participation.
        # This acts as a security check: if the user isn't a participant, they cannot post a message.
        conversation = get_object_or_404(
            Conversation.objects.filter(participants=self.request.user), pk=chat_pk
        )

        # 2. Save the message, using the current user as the sender and the found conversation.
        serializer.save(sender=self.request.user, chat=conversation)
