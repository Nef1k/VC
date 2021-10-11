import logging
from smtplib import SMTPAuthenticationError

from django.db.models.signals import post_delete
from django.dispatch import receiver

from contacts.actions import send_contact_removal_email
from contacts.models import Contact


@receiver(post_delete, sender=Contact)
def send_email(sender, instance, **kwargs):
    """Send email notification each time contact is deleted."""
    try:
        send_contact_removal_email(instance)
    except Exception as e:
        logging.error(f'Could not send an email: {str(e)}')
