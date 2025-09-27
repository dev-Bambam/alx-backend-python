import logging
from datetime import datetime, time, timedelta
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponseForbidden, JsonResponse # Added for 403 and rate limiting

# --- Configuration for Rate Limiting ---
# Global dictionary to store request times for rate limiting
# Key: IP Address (str); Value: List of timestamps (datetime objects)
IP_REQUEST_LOG = {}
MAX_REQUESTS = 5
TIME_WINDOW_SECONDS = 60 # 1 minute

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
            # Use __str__ or get_username for the User object
            username = str(user) if hasattr(user, '__str__') else user.get_username()
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
        # Define the allowed window (UTC hours)
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


class OffensiveLanguageMiddleware:
    """
    Middleware that implements rate limiting (5 POST messages per minute per IP).
    This restricts the number of messages a user can send within a short period to prevent spamming.
    """
    def __init__(self, get_response):
        self.get_response = get_response
    
    def get_client_ip(self, request):
        """Utility function to extract client IP, handling proxies."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            # If multiple IPs are listed (due to proxies), take the first one
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            # Otherwise, use the remote address
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def __call__(self, request):
        # Rate limiting only applies to POST requests (i.e., sending a new message/chat)
        if request.method == 'POST':
            ip = self.get_client_ip(request)
            now = datetime.now()
            
            # Initialize or clean up the log for this IP
            if ip not in IP_REQUEST_LOG:
                IP_REQUEST_LOG[ip] = []
            
            # 1. Clean up old requests (older than TIME_WINDOW_SECONDS)
            one_minute_ago = now - timedelta(seconds=TIME_WINDOW_SECONDS)
            # Filter out timestamps that are outside the window
            IP_REQUEST_LOG[ip] = [t for t in IP_REQUEST_LOG[ip] if t > one_minute_ago]
            
            # 2. Check the limit
            if len(IP_REQUEST_LOG[ip]) >= MAX_REQUESTS:
                # Limit exceeded: deny the request immediately with HTTP 429
                return JsonResponse(
                    {"detail": f"Rate limit exceeded: Max {MAX_REQUESTS} requests per {TIME_WINDOW_SECONDS} seconds."},
                    status=429
                )
            
            # 3. If within the limit, log the current request time
            IP_REQUEST_LOG[ip].append(now)

        # Proceed to the next middleware or the view
        response = self.get_response(request)
        return response
