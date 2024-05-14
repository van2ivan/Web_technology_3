from datetime import datetime

from celery import shared_task
from celery.result import AsyncResult
from django.core.mail import send_mail
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import Contact

sender = "Ivan Ius"


def execute_task(data):
    res: AsyncResult = create_new_contact.delay(data)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'admin',
        {'type': 'send_message',
         'message': f'task: {res.task_id}, data: {res.result}, finished: {datetime.now()},'
                    f' successful: {res.successful()}'}
    )


@shared_task
def create_new_contact(data):
    new_contact = Contact.objects.create(phone_number=data.get('phone_number'), contact_name=data.get('contact_name'),
                                         user_id=data.get('user_id'), email=data.get('email'))
    print(new_contact)
    send_mail('New contact created', f'There is yours new created contact:'
                                     f' {new_contact.contact_name} {new_contact.phone_number}',
              sender, [new_contact.user.email])
    return {'username': new_contact.user.username, "contact_name": new_contact.contact_name,
            'phone_number': new_contact.phone_number}
