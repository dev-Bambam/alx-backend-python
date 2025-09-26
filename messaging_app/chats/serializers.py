from .models import Message, Chat
from rest_framework import serializers
from django.contrib.auth.models import User


class MessageSerializer(serializers.ModelSerializer):
    # Use a custom field get the username instead of user's id
    sender = serializers.ReadOnlyField(source="sender.username")

    class Meta:
        model = Message
        fields = ["id", "sender", "content", "timestamp"]
        read_only_fields = ["sender", "chat"]


class ChatSerializer(serializers.ModelSerializer):
    # The crucial part: this field nests the MessageSerializer.
    # The `many=True` argument tells it to expect multiple messages.
    # The `read_only=True` argument prevents a client from creating messages this way.
    messages = MessageSerializer(many=True, read_only=True)

    # we will get a list of username instead of user IDs
    participants = serializers.SlugRelatedField(
        many=True,
        slug_field='username',
        queryset=User.objects.all(),
        required = False
    )

    class Meta:
        model = Chat
        fields = ['id', 'participants', 'title' , 'created_at', 'messages']
