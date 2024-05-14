from rest_framework.permissions import BasePermission

from .models import User, Contact


class IsOwner(BasePermission):
    message = 'You do not have permission to perform this action.'

    def has_permission(self, request, view):
        user: User = request.user
        contact = Contact.objects.filter(id=request.parser_context['kwargs']['pk'], user=user).first()
        if contact is None:
            return False
        return True
