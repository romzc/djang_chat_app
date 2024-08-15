from datetime import date
from django.db import transaction
from django.contrib.auth.models import User
from chats.models import Contact, Message


@transaction.atomic
def create_contact(*,user: User, contact: User) -> Contact:
    user_contact = Contact(user=user, contact=contact)
    user_contact.full_clean()
    user_contact.save()
    return user_contact

@transaction.atomic
def create_message(*, user: User, recevier: User, content: str) -> Message:
    message = Message(user=user, recevier=recevier, content=content)
    message.full_clean()
    message.save()
    return message
