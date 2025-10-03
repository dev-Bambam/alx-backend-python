from django.http import HttpResponseForbidden, HttpResponseBadRequest, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
import logging
from django.db.models import Q
from .models import Message

logger = logging.getLogger(__name__)
User = get_user_model()

@login_required
def delete_user_account(request):
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated:
            return HttpResponseForbidden('Authentication is required to this action')
        
        try:
            user_id = user.id
            user_email = user.email

            user.delete()

            # Since the user is now deleted, we log them out and send a success message.
            # In a real API, this would return a 204 No Content response
            return HttpResponse(status=200)
        except Exception as e:
            return HttpResponseBadRequest('An error occured during account deletion', status=400)
    else:
        return HttpResponseBadRequest('Method not allowed. Use POST to confirm deletion', status=405)

def serialize_message(message):
    '''
    Helper function to convert a Message object into a serialiazable dictionary
    '''
    return {
        'id': message.id,
        'sender': message.sender.email,
        'reciever': message.reciever.email,
        'content': message.content,
        'timestamp': message.timestamp.isoformat(),
        'edited': message.edited,
        'parent_id': message.parent_message_id,
        # Recursuvely include replies (children)
        'replies': [serialize_message(reply) for reply in message.replies.all()]
    }

@login_required
def get_threaded_messages(request):
    sender = request.user
    '''
    Fetches all top-level messages and their replies efficiently,
    demonstrating select_related and prefetch_related
    '''

    # start by filtering for only top-level (those with no parent)
    top_level_messages = Message.objects.filter(
        parent_message__isnull=True
    ).filter(
        # Filter: User must be involved as sender OR receiver of the top message
        Q(sender=request.user) | Q(receiver=request.user)
    ).select_related(
        sender,
        'reciever'
    ).prefetch_related(
        # Use bulk query to fetch all immediate replies for the entire queryset
        'replies',             
        # Deep prefetching: For the replies, also pre-fetch their sender and receiver
        'replies__sender',
        'replies__receiver',
        # Go one level deeper (replies of replies)
        'replies__replies',
        'replies__replies__sender'
        # Note: You can continue this nesting, but usually 2-3 levels are enough
    ).order_by('-timestamp')
    
    # -----------------------------------------------------------
    # 2. RECURSIVE DATA STRUCTURING (Python Logic)
    # The prefetch_related manager automatically attaches the replies to the parent 
    # message instance (e.g., message.replies is already pre-loaded).
    # We serialize the data recursively to create the nested structure (tree).
    #

    threaded_data = [
        serialize_message(message) for message in top_level_messages
    ]

    # Returning the data as a JSON response
    return JsonResponse(
        {'threads': threaded_data},
        status = 200
    )

@login_required
def get_unread_message(request):
    unread_message_qs = Message.unread_objects.unread_for_user(request.user).only(
        'id',
        'sender',
        'content',
        'timestamp'
        'read'
    ).select_related(
        'sender'
    ).order_by('timestamp')

    unread_data = [{
        'id': msg.id,
        'sender_email': msg.sender.email,
        'content': msg.content,
        'timestamp': msg.timestamp.isoformat(),
        'read': msg.read
    } for msg in unread_message_qs]

    return JsonResponse(
        {'unread_inbox': unread_data},
        status = 200
    )