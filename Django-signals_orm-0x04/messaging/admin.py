from django.contrib import admin

from .models import Message, Notification


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "content_preview", "timestamp")
    list_filter = ("sender", "reciever", "timestamp")
    search_fields = ("content", "sender__email", "reciever__email")
    ordering = ("-timestamp",)

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    
    content_preview.short_description = 'content'

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message_sender', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at', 'user')
    search_fields = ('user__email', 'message__content')
    ordering = ('-created_at',)

    def message_sender(self, obj):
        return obj.message.sender.email
    message_sender.short_description = 'Message Sender'
