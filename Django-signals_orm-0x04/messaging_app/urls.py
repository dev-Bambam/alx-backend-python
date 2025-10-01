from django.urls import path
from ..messaging.views import delete_user_account

urlpatterns = [
    path(
        'user/delete/',
        delete_user_account,
        name = 'delete_user_account'
    )
]