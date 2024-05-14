from django.shortcuts import get_object_or_404
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.decorators import database_sync_to_async
from djangochannelsrestframework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
)
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Contact, User
from .consumer_serializer import ContactSerializer
from .consumer_permissions import ContactPermissions, is_user_logged_in


@database_sync_to_async
def update_user_incr(user):
    if is_user_logged_in(user):
        User.objects.filter(pk=user.pk).update(is_online=True)


@database_sync_to_async
def update_user_decr(user):
    if is_user_logged_in(user):
        User.objects.filter(pk=user.pk).update(is_online=False)


class ActivityStatusConsumer:

    async def connect(self):
        await self.accept()
        await update_user_incr(self.scope['user'])

    async def disconnect(self, code):
        await update_user_decr(self.scope['user'])


class ContactConsumer(ActivityStatusConsumer, GenericAsyncAPIConsumer, RetrieveModelMixin, ListModelMixin,
                      CreateModelMixin):
    queryset = Contact.objects.all()
    permission_classes = (ContactPermissions, )
    serializer_class = ContactSerializer

    def get_serializer_class(self, **kwargs):
        return ContactSerializer

    def get_queryset(self, **kwargs):
        if kwargs.get('action') == 'list':
            constacts = Contact.objects.filter(user=self.scope['user'])
            return constacts
        return Contact.objects.all()

    def perform_create(self, serializer, **kwargs):
        new_contact = Contact.objects.create(contact_name=serializer.data.get('contact_name'),
                                             email=serializer.data.get('email'),
                                             phone_number=serializer.data.get('phone_number'),
                                             user=self.scope['user'])
        return new_contact


class NotifyAdminConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()
        await update_user_incr(self.scope['user'])
        await self.channel_layer.group_add(
            'admin',
            self.channel_name,
        )

    async def disconnect(self, code):
        await update_user_decr(self.scope['user'])

    async def send_message(self, event):
        message = event['message']
        await self.send(text_data=message)
