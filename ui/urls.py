from django.urls import path

from ui import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('contacts/delete/<int:pk>', views.DeleteContactView.as_view(), name='contact-delete'),
    path('contacts/add', views.AddContactView.as_view(), name='contact-add'),

    path('sign_in/', views.SignInView.as_view(), name='sign-in'),
    path('logout/', views.LogoutView.as_view(), name='logout')
]
