import logging
from datetime import datetime
from django.contrib.auth.models import AnonymousUser

# Get the custom logger we defined in the settings.py
request_logger = logging.getLogger('request_logger')

class RequestLoggingMiddleware:
    '''
    MW to log information about every incoming request.
    It runs after the view has executed, ensuring request.user is available
    '''

    def __init__(self, get_response):
        '''One time configuration and initialization. Stores the get_response callable'''
        self.get_response = get_response

    def __call__(self, request):
        '''The request processing logic happens here. This is run on every request'''

        # Pass the request to the next middleware or the view
        response = self.get_response(request)

        # --- Logging Phase (runs after view execution) ---

        # Determine the username, (handling AnonymousUser gracefully)
        user = request.user
        username = 'Anonymous'
        if user and user.is_authenticated:
            username = user.get_username()
        elif user and isinstance(user, AnonymousUser):
            username = 'Anonymous'

        #  Log the require information in the specified format
        log_message = (
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - "
            f"User: {username} - "
            f"Path: {request.path} - "
            f"Method: {request.method}"
        )

        # Write the log message to the file
        request_logger.info(log_message)

        # return th response up the stack
        return response