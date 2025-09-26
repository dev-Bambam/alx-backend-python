from rest_framework import permissions

class IsAuthenticatedAndOwner(permissions.BasePermission):
    '''Custom permission to only allow owners of an object to view or edit it'''

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any authenticated user,
        # but write permissions are only allowed to the owner of the project
        return request.user and obj.user == request.user
    
class isParticipantOfConversation(permissions.BasePermission):
    '''Custom permission to allow a participant in a conversation to access it'''

    def has_permission(self, request, view):
        # Allow only authenitcated user to access the API
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Allow participants to view, update, and delete messages.
        # This will be used for specific objects (messages or conversations).

        # Read permissions are always allowed for authenticated participants
        if request.method in permissions.SAFE_METHODS:
            return obj.user == request.user
        
        # Write permissions (PUT, PATCH, DELETE) are restricted to the owner.
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return obj.user == request.user
        
        return False