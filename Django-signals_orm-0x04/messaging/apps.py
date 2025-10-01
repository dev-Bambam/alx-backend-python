from django.apps import AppConfig


class MessagingConfig(AppConfig):
    # Set the primary key field type
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'messaging'

    def ready(self):
        '''
        This method is called when django starts up.
        It's required to import the signals file and connect the recievers
        '''
        import messaging.signals