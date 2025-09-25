from rest_framework import permissions

class isAuthenticatedAndOwner(permissions.BasePermission):
    '''Custom permission to only allow owners of an object to view or edit it'''

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any authenticated user,
        # but write permissions are only allowed to the owner of the project
        return request.user and obj.user == request.user