from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory
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

@receiver(pre_save, sender=Message)
def log_message_pre_save(sender, instance, **kwargs):
    '''
    Fires BEFORE a Message is saved to the database.
    If the instance already exists (has a primary key), we for content changes
    '''

    # Check if the instance is an existing object being updated ( it has a primary key)

    if instance.pk:
        try:
            original_instance = Message.objects.get(pk=instance.pk)

            # check if the content has actually changed
            if original_instance.content != instance.content:
                # create a history record with the OLD content
                MessageHistory.objects.create(
                    message = instance,
                    old_content = original_instance.content
                )
                logger.info(
                    f'Message ID {instance.pk} content changed'
                    f"Old version logged to history"
                )

                # Update the 'edited' flag on the instance about to be saved
                instance.edited = True
        except Message.DoesNotExist:
            # should not happen often, but handle cas where PK exists but ibject is missing
            logger.warning(f'Message ID {instance.pk} not found during pre_save log')
        except Exception as e:
            logger.error(f'Unhandled error in pre_save signal: {e}')