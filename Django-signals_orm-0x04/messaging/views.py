from django.shortcuts import render
from django.http import HttpResponseForbidden, HttpResponseBadRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
import logging

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
