from django.conf import settings
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api import views


urlpatterns = [
    path('contacts/', views.ContactsListView.as_view(), name='contact-list'),
    path('contacts/<int:pk>/', views.ContactsDetailsView.as_view(), name='contact-details'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


if settings.DEBUG:
    urlpatterns.append(path('', views.swagger_schema_view.with_ui('swagger'), name='swagger-ui'),)
