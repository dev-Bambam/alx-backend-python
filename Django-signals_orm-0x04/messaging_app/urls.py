from django.urls import path
from ..messaging.views import delete_user_account, get_unread_message

urlpatterns = [
    path(
        'user/delete/',
        delete_user_account,
        name = 'delete_user_account'
    ),
    path(
        'user/unread-messages/',
        get_unread_message,
        name = 'get_unread_message'
    )
]