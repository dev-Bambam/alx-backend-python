from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification
import logging

# set up a logger for signal  tracking
logger = logging.getLogger(__name__)

@receiver(post_save, sender=Message)
def create_notification_on_new_message(sender, instance, created, **kwargs):
    '''
    Receiver function that fires AFTER a Message instance is saved. 

    Arugements:
    - sender: The Message class (the model that sent the signal)
    - instance: the actual Message object that was just saved
    - created: Boolean. True if the object was just created; False if it was updated
    - **kwargs: Other arguments provided by the signal
    '''

    # We only want to create a notification when a message is brand NEW
    # not every time existing message is updated
    if created:
        try:
            # The 'reciever' of the message is the 'user' who should be notified
            Notification.objects.create(
                user=instance.receiver,
                message=instance
            )
            logger.info(
                f'Notification created for {instance.receiver.email}'
                f'due to new message from {instance.sender.email}'
            )
        except Exception as e:
            logger.error(f'Error creating notification: {e}')