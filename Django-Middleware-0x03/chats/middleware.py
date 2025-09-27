import logging
from datetime import datetime, time
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponseForbidden # Added for 403 response

# Get the custom logger we defined in settings.py
request_logger = logging.getLogger('request_logger')

class RequestLoggingMiddleware:
    """
    Middleware to log information about every incoming request.
    It runs after the view has executed, ensuring request.user is available.
    """


    def __init__(self, get_response):
        """
        One-time configuration and initialization. Stores the get_response callable.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        The request processing logic happens here. This is run on every request.
        """
        
        # Pass the request to the next middleware or the view
        response = self.get_response(request)
        
        # --- Logging Phase (runs after view execution) ---
        
        # Determine the username (handling AnonymousUser gracefully)
        user = request.user
        username = 'Anonymous'
        if user and user.is_authenticated:
            username = user.get_username()
        elif user and isinstance(user, AnonymousUser):
             username = 'Anonymous'
        
        # Log the required information in the specified format
        log_message = (
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - "
            f"User: {username} - "
            f"Path: {request.path} - "
            f"Method: {request.method}"
        )
        
        # Write the log message to the file
        request_logger.info(log_message)

        # Return the response up the stack
        return response


class RestrictAccessByTimeMiddleware:
    """
    Middleware to restrict access to the API outside of peak hours (6 AM to 9 PM).
    Denies access with a 403 Forbidden response between 9 PM (21:00) and 6 AM (06:00) UTC.
    """
    def __init__(self, get_response):
        """
        One-time configuration and initialization. Stores the get_response callable 
        and defines the restriction window.
        """
        self.get_response = get_response
        # Define the restriction window (UTC hours)
        self.start_hour = time(6, 0, 0)  # 6:00 AM
        self.end_hour = time(21, 0, 0)   # 9:00 PM (21:00)

    def __call__(self, request):
        """
        The request processing logic happens here. This is run on every request.
        """
        # Get the current time (uses the TIME_ZONE set in settings, default is UTC)
        now = datetime.now().time()
        
        # Check if the current time is OUTSIDE the allowed window (6 AM to 9 PM).
        # Restriction applies if: time < 6 AM OR time >= 9 PM
        if now < self.start_hour or now >= self.end_hour:
            # Deny access by returning a 403 Forbidden response immediately
            return HttpResponseForbidden(
                "Access restricted. The messaging service is available only between 6:00 AM and 9:00 PM UTC."
            )

        # If time is within the allowed window, proceed to the next middleware or the view.
        response = self.get_response(request)
        
        return response
