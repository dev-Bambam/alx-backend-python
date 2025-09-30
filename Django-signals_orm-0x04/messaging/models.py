from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

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
    content = models.TextField()
    timestamp = models.DateTimeField(
        default=timezone.now,
        editable=False
    )

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