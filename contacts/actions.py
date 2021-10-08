from django.conf import settings
from django.core.mail import send_mail
from django.db.models import QuerySet

from contacts.models import Contact
from users.models import User


def create_contact(issuer: User, name: str, email: str) -> None:
    if not issuer.has_perm('add_contact'):
        raise PermissionError

    new_contact = Contact(name=name, email=email)
    new_contact.save()


def update_contact(issuer: User, contact_id: int, name: str, email: str) -> None:
    if not issuer.has_perm('change_contact'):
        raise PermissionError

    contact = Contact.objects.get(contact_id)
    contact.name = name
    contact.email = email
    contact.save()


def get_contact(issuer: User, contact_id: int) -> Contact:
    if not issuer.has_perm('view_contact'):
        raise PermissionError

    return Contact.objects.get(pk=contact_id)


def get_contacts(issuer: User) -> QuerySet:
    if not issuer.has_perm('view_contacts'):
        raise PermissionError

    return Contact.objects.all()


def delete_contact(issuer: User, contact_id: int) -> None:
    if not issuer.has_perm('delete_contact'):
        raise PermissionError

    contact = Contact.objects.get(pk=contact_id)
    contact.delete()


def send_contact_removal_email(contact: Contact):
    subject = 'Contact was removed'
    message = f'Contact <b>"{contact.name}"</b> was removed from the list.'
    to = settings.NOTIFICATION_EMAIL

    send_mail(
        subject=subject,
        from_email=None,  # use the one from settings
        message=message,
        html_message=message,
        recipient_list=[to]
    )
