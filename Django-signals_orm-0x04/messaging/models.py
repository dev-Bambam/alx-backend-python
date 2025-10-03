from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from .managers import UnreadMessagesManager

# Get the active User model for the Foreign Key relationaship
User = get_user_model()

class Message(models.Model):
    '''
    Rep a communication sent from one user to another 
    This model acts as the SENDER of the post_save signal
    '''
    sender = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='sent_messages',
        verbose_name='Sender'
    )
    receiver = models.ForeignKey(
        User,
         on_delete=models.CASCADE,
         related_name='recieved_messages',
         verbose_name='Reciever'
    )
    # This is call 'Adjacency List where a model reference itself
    # we are using this for threaded conversation to store replies to a message
    parent_message = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='replies',
        verbose_name='Reply to'
    )
    content = models.TextField()
    timestamp = models.DateTimeField(
        default=timezone.now,
        editable=False
    )
    edited = models.BooleanField(default=False)
    read = models.BooleanField(default=False)

    # Register Custom Mangers
    objects = models.Manager()
    unread_objects = UnreadMessagesManager()
    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ['-timestamp']

    def __str__(self):
        return f'Message from {self.sender} to {self.receiver} {self.timestamp.strftime('%H:%M')}'

class Notification(models.Model):
    '''
    Rep a notification created automatically when a new Message is recieved.
    This model is the product of the signal RECIEVER function
    '''
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='Notified User'
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='notification_entry',
        verbose_name='Source Message'
    )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(
        default=timezone.now, 
        editable=False
    )

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']

    def __str__(self):
        read_status = "READ" if self.is_read else 'NEW'
        return f'[{read_status}] New message from {self.message.sender}'
    
class MessageHistory(models.Model):
    """
    Stores the previous content of a Message before an update occurs.
    This model is populated by the pre_save signal.
    """
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='history', # Allows access: message.history.all()
        verbose_name='Original Message'
    )
    old_content = models.TextField()
    # Records when the update happened (not when the original message was sent)
    edited_at = models.DateTimeField(default=timezone.now) 
    edited_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    class Meta:
        verbose_name = "Message History"
        verbose_name_plural = "Message History"
        ordering = ['-edited_at']

    def __str__(self):
        return f"History of {self.message.id} saved at {self.edited_at.strftime('%Y-%m-%d %H:%M')}"
