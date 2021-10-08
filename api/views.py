from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import generics, permissions

from api.serializers import ContactSerializer
from contacts.models import Contact


class ContactsListView(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class ContactsDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


swagger_schema_view = get_schema_view(
    openapi.Info(
        title='Contacts API',
        default_version='v1',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
