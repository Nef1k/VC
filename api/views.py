from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated

from VoxieContacts.permissions import GET, HasPerm, POST, PUT, PATCH, DELETE
from api.serializers import ContactSerializer
from contacts.models import Contact


class ContactsListView(generics.ListCreateAPIView):
    """API to create and list instances of Contact."""

    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated,
                          (GET & HasPerm('contacts.view_contact'))
                          | (POST & HasPerm('contacts.add_contact'))]


class ContactsDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """API to retrieve, update and remove instances of Contact."""

    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated,
                          (GET & HasPerm('contacts.view_contact'))
                          | ((PUT | PATCH) & HasPerm('contacts.change_contact'))
                          | (DELETE & HasPerm('contacts.delete_contact'))]


# Swagger view.
swagger_schema_view = get_schema_view(
    openapi.Info(
        title='Contacts API',
        default_version='v1',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
