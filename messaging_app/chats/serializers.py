from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Conversation, Message

# Get the custom User model defined in chats/models.py
User = get_user_model()
# --- 1. ReadUserSerializer ---
# A minimal serializer used for nesting (e.g., displaying the sender or participants)
# This keeps nested ouput cleand and prevents exposing too much user data.
class ReadUserSerializer(serializers.ModelSerializer):
    '''Serializer for read-only user data'''

    class Meta:
        model = User
        fields = ('user_id', 'email', 'first_name', 'last_name', 'role')
        read_only_fields = fields


# ---2. MessageSerializer ---
class MessageSerializer(serializers.ModelSerializer):
    '''Serializer for Message creation and retrieval'''

    # Nested fields to display the sender's details when reading a message
    # The sender field is read_only, as the sender is determined by the logged-in user.
    sender = ReadUserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = (
            'message_id',
            'chat',
            'sender',
            'message_body',
            'sent_at'
        )
        read_only_fields = (
            'message_id',
            'sender',
            'sent_at'
        )

        def validate_chat(self, chat_id):
            '''
            Validate that the conversation exists.
            '''
            if not Conversation.objects.filter(pk=chat_id).exists():
                raise serializers.ValidationError('Conversation not found')
            return chat_id
        
# --- 3. ConversationSerializer ---
class ConversationSerializer(serializers.ModelSerializer):
    '''Serializer for Conversation listing, creating and detailed retrieval'''
    # CRITICAL: Nested relationship to include message in the conversation detail view
    # many=True means this is a list of Message objects
    # read_only=True ensures we don;t try to create/update messages here
    messages = MessageSerializer(many=True, read_only=True)

    # Used for listing participants in read views (GET)
    paritcipants = ReadUserSerializer(many=True, read_only=True)

    # For creation (POST), we need a field that accepts USer IDs
    # This write-only field overrides the read-only 'participants' field above for creation
    paritcipant_id = serializers.ListField(
        child=serializers.UUIDField(),
        write_only =True,
        help_text='List of UUIDs for users participating in the conversation'
    )

    class Meta:
        model=Conversation
        fields=(
            'conversation_id',
            'title',
            'participants', # Nested list of users (Read only)
            'participant_ids', # List of UUIDs for creation (write only)
            'created_at',
            'messages' # Nested list of messages (Read Only)
        )
        read_only_fields = ('conversation_id', 'created_at')
    
    def create(self, validated_data):
        '''Custom create method to handle the many-to-many participants relationship
        '''
        participant_ids = validated_data.pop('participants_ids', [])

        # 1. Create the Conversation instance without the participants
        conversation = Conversation.objects.create(**validated_data)

        # 2. Add participants using IDs
        if participant_ids:
            # Add the participants to many-to-many field
            conversation.participants.set(participant_ids)

            return conversation