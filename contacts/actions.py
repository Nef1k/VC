from django.conf import settings
from django.core.mail import send_mail
from django.db.models import QuerySet

from contacts.models import Contact
from users.models import User


def create_contact(issuer: User, name: str, email: str) -> None:
    """
    Create a contact.

    Args:
        issuer: User who is trying to create a contact.
        name: Contact name.
        email: Contact email.

    Raises
        PermissionError: when user has no add_contact permission.

    """
    if not issuer.has_perm('contacts.add_contact'):
        raise PermissionError

    new_contact = Contact(name=name, email=email)
    new_contact.save()


def update_contact(issuer: User, contact_id: int, name: str, email: str) -> None:
    """
    Update a contact.

    Args:
        issuer: User who is trying to create a contact.
        contact_id: ID of the contact which is to be updated.
        name: New contact name.
        email: New contact email.

    Raises
        PermissionError: when user has no change_contact permission.

    """
    if not issuer.has_perm('contacts.change_contact'):
        raise PermissionError

    contact = Contact.objects.get(contact_id)
    contact.name = name
    contact.email = email
    contact.save()


def get_contact(issuer: User, contact_id: int) -> Contact:
    """
    Retrieve a contact with given ID.

    Args:
        issuer: User who is trying to create a contact.
        contact_id: ID of the contact which is to be retrieved.

    Raises
        PermissionError: when user has no view_contact permission.

    """
    if not issuer.has_perm('contacts.view_contact'):
        raise PermissionError

    return Contact.objects.get(contact_id)


def get_contacts(issuer: User) -> QuerySet:
    """
    Retrieve all contacts.

    Args:
        issuer: User who is trying to create a contact.

    Raises
        PermissionError: when user has no view_contact permission.

    """
    if not issuer.has_perm('contacts.view_contact'):
        raise PermissionError

    contact_list = Contact.objects.all()
    return contact_list.order_by('-id')


def delete_contact(issuer: User, contact_id: int) -> None:
    """
    Delete contact with given ID.

    Args:
        issuer: User who is trying to create a contact.
        contact_id: ID of the contact which is to be deleted.

    Raises
        PermissionError: when user has no delete_contact permission.

    """
    if not issuer.has_perm('contacts.delete_contact'):
        raise PermissionError

    contact = Contact.objects.get(pk=contact_id)
    contact.delete()


def send_contact_removal_email(contact: Contact):
    """
    Send an email notification of contact deletion.

    Args:
        contact: Contact which was just deleted.

    """
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
