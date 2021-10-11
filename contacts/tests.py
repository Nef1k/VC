from unittest.mock import MagicMock, patch

from django.conf import settings
from django.test import TestCase

from contacts import actions


class ContactBaseTestCase(TestCase):
    def setUp(self) -> None:
        self.user = MagicMock()
        self.user.has_perm_return_value = True


@patch('contacts.actions.Contact')
class CreateContactTests(ContactBaseTestCase):
    def test_permission_required(self, *args, **kwargs):
        """Check if has_perm was called with `contacts.add_contact` permission."""
        actions.create_contact(self.user, name='Test', email='test@example.com')
        self.user.has_perm.assert_called_with('contacts.add_contact')

    def test_contact_creation(self, contact_mock, *args, **kwargs):
        """Check if Contact instance was create with given values."""
        contact_name = 'Test'
        contact_email = 'foo@bar.com'
        contact_instance = MagicMock()
        contact_mock.return_value = contact_instance

        actions.create_contact(self.user, name=contact_name, email=contact_email)

        contact_mock.assert_called_with(name=contact_name, email=contact_email)
        contact_instance.save.assert_called_once()


@patch('contacts.actions.Contact')
class UpdateContactTests(ContactBaseTestCase):
    def test_permission_required(self, *args, **kwargs):
        """Check if has_perm was called with `contacts.change_contact` permission."""
        actions.update_contact(self.user, 1, 'foo', 'bar')
        self.user.has_perm.assert_called_with('contacts.change_contact')

    def test_contact_update(self, contact_mock, *args, **kwargs):
        """Check if given contact was update with given value."""
        contact_id = 42
        new_name = 'Test'
        new_email = 'foo@bar.com'
        contact_instance = MagicMock()
        contact_mock.objects.get.return_value = contact_instance

        actions.update_contact(self.user, contact_id, name=new_name, email=new_email)

        contact_mock.objects.get.assert_called_with(contact_id)
        assert contact_instance.name == new_name
        assert contact_instance.email == new_email
        contact_instance.save.assert_called_once()


@patch('contacts.actions.Contact')
class GetContactTests(ContactBaseTestCase):
    def test_permission_required(self, *args, **kwargs):
        """Check if has_perm was called with `contacts.view_contact` permission."""
        actions.get_contact(self.user, 1)
        self.user.has_perm.assert_called_with('contacts.view_contact')

    def test_contact_retrieve(self, contact_mock, *args, **kwargs):
        """Check if given contact was retrieved."""
        contact_id = 42

        actions.get_contact(self.user, contact_id)

        contact_mock.objects.get.assert_called_with(contact_id)


@patch('contacts.actions.Contact')
class GetContactsTests(ContactBaseTestCase):
    def test_permission_required(self, *args, **kwargs):
        """Check if has_perm was called with `contacts.view_contact` permission."""
        actions.get_contact(self.user, 1)
        self.user.has_perm.assert_called_with('contacts.view_contact')

    def test_contact_retrieve(self, contact_mock, *args, **kwargs):
        """Check if give all contacts was retrieved."""
        actions.get_contacts(self.user)

        contact_mock.objects.all.assert_called_once()


@patch('contacts.actions.send_contact_removal_email')
@patch('contacts.actions.Contact')
class DeleteContactTests(ContactBaseTestCase):
    def test_permission_required(self, *args, **kwargs):
        """Check if has_perm was called with `contacts.delete_contact` permission."""
        actions.delete_contact(self.user, 1)
        self.user.has_perm.assert_called_with('contacts.delete_contact')

    def test_contact_delete(self, contact_mock, send_mail_mock, *args, **kwargs):
        """Check if given contact was deleted."""
        contact_id = 42
        contact_instance = MagicMock()
        contact_mock.objects.get.return_value = contact_instance

        actions.delete_contact(self.user, contact_id)

        contact_mock.objects.get.assert_called_with(pk=contact_id)
        contact_instance.delete.assert_called_once()


@patch('contacts.actions.send_mail')
class SendRemovalMailTests(TestCase):
    def test_email_sending(self, send_mail_mock):
        """Check if correct email is sent for given contact."""
        contact_name = 'Test'

        contact_instance = MagicMock()
        contact_instance.name = contact_name

        actions.send_contact_removal_email(contact_instance)

        send_mail_mock.assert_called_with(
            subject='Contact was removed',
            from_email=None,
            message=AnyStringWith(contact_name),
            html_message=AnyStringWith(contact_name),
            recipient_list=[settings.NOTIFICATION_EMAIL],
        )


class AnyStringWith(str):
    def __eq__(self, other):
        return self in other
