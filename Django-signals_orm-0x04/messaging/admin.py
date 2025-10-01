from django.contrib import admin

from .models import Message, Notification, MessageHistory


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

@admin.register(MessageHistory) # Register the history model separately
class MessageHistoryAdmin(admin.ModelAdmin):
    list_display = ('message', 'old_content_preview', 'edited_at')
    list_filter = ('edited_at',)
    search_fields = ('message__content', 'old_content')
    ordering = ('-edited_at',)

    def old_content_preview(self, obj):
        return obj.old_content[:50] + '...' if len(obj.old_content) > 50 else obj.old_content
    old_content_preview.short_description = 'Previous Content'