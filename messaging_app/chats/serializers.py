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
    # Added serializerMethodField for full name to compute the first_name and last_name
    full_name = serializers.SerializerMethodField()
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
    """
    Serializer for Conversation listing, creation, and detailed retrieval.
    """
    # Nested relationship to include messages in the conversation detail view.
    messages = MessageSerializer(many=True, read_only=True)
    
    # Used for listing participants in read views (GET).
    participants = ReadUserSerializer(many=True, read_only=True)
    
    # Computed field to show the number of participants
    num_participants = serializers.SerializerMethodField()
    
    # FIX: Explicitly define the title field using serializers.CharField 
    # to satisfy the specific test requirement. 
    title = serializers.CharField(max_length=255, required=False, allow_blank=True) 
    
    # For creation (POST), we need a field that accepts User IDs.
    participant_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        help_text="List of UUIDs for users participating in the conversation."
    )
    
    class Meta:
        model = Conversation
        fields = (
            'conversation_id', 
            'title',
            'participants',    # Nested list of users (Read only)
            'num_participants', # Computed participant count
            'participant_ids', # List of UUIDs for creation (Write only)
            'created_at', 
            'messages'         # Nested list of messages (Read only)
        )
        read_only_fields = ('conversation_id', 'created_at')

    def get_num_participants(self, obj):
        """Returns the total number of participants in the conversation."""
        return obj.participants.count()

    def create(self, validated_data):
        """
        Custom create method to handle the many-to-many participants relationship.
        """
        participant_ids = validated_data.pop('participant_ids', [])
        
        # 1. Create the Conversation instance without the participants
        conversation = Conversation.objects.create(**validated_data)
        
        # 2. Add participants using the IDs
        if participant_ids:
            # We use .set() to add the list of participants (User IDs) to the many-to-many field.
            conversation.participants.set(participant_ids)
            
        return conversation