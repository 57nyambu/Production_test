from rest_framework import permissions

class HasActiveSubscription(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            hasattr(request.user, 'subscription') and 
            request.user.subscription.is_active
        )