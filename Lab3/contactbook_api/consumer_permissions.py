from djangochannelsrestframework.permissions import BasePermission
from django.contrib.auth.models import AnonymousUser


def is_user_logged_in(user):
    return not isinstance(user, AnonymousUser)


class ContactPermissions(BasePermission):
    def has_permission(self, scope, consumer, action, **kwargs):
        print(action)
        print(is_user_logged_in(scope['user']))
        print(scope['user'])
        if action in ['create', 'list', 'retrieve'] and is_user_logged_in(scope['user']):
            return True
        return False
