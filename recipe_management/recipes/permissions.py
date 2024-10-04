from rest_framework import permissions

class IsRecipeOwner(permissions.BasePermission):
    # Custom permission to allow only the owner of the recipe to edit/ delete it.

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user