from rest_framework import permissions

class isAuthenticatedAndOwner(permissions.BasePermission):
    '''Custom permission to only allow owners of an object to view or edit it'''

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any authenticated user,
        # but write permissions are only allowed to the owner of the project
        return request.user and obj.user == request.user
    
class isParticipantOfConversation(permissions.BasePermission):
    '''Custom permission to allow a participant in a conversation to access it'''

    def has_object_permission(self, request, view, obj):
        # Check if the user is one of the participants in the conversation.
        # This assumes your Chat model has a 'participants' field.
        # For a simple user model, this means checking if the user is the owner.
        # For a more complex model, you'd check a ManyToManyField.
        # For this task, we will assume the conversation is linked to a user via ForeignKey
        # and they are therefore a participant.

        if hasattr(obj, 'chat'):
            chat = obj.chat
        else:
            chat = obj

        return chat.user == request.user or request.user in chat.participants.all() if hasattr(chat, 'participant') else chat.user == request.user