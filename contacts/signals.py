from django.db.models.signals import post_delete
from django.dispatch import receiver

from contacts.actions import send_contact_removal_email
from contacts.models import Contact


@receiver(post_delete, sender=Contact)
def send_email(sender, instance, **kwargs):
    send_contact_removal_email(instance)
    print('Email sent!')
