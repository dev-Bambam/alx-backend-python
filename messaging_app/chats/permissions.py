from rest_framework import permissions

class IsConversationParticipant(permissions.BasePermission):
    '''Custom permission to only allow participants of a conversation to view, update, or delete it'''

    def has_object_permission(self, request, view, obj):
        # Allow read permissions (GET, HEAD, OPTIONS) for participants
        if request.method in permissions.SAFE_METHODS:
            return request.user in obj.participants.all()
        
        # Write permissions (PUT, PATCH, DELETE) are only allowed
        #  if the user is a participant
        return request.user in obj.participants.all()