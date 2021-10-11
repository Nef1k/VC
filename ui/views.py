from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from contacts.actions import delete_contact, create_contact, get_contacts
from contacts.models import Contact
from ui.errors import ResponseError
from ui.forms import ContactForm
from ui.utils import reverse


class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        contacts = get_contacts(request.user)
        return render(request, 'index.html', context={
            'contacts': contacts,
            'can_view': request.user.has_perm('contacts.view_contact'),
            'can_add': request.user.has_perm('contacts.add_contact'),
            'can_delete': request.user.has_perm('contacts.delete_contact'),
        })


class AddContactView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'contacts.add_contact'

    def get(self, request):
        contact_form = ContactForm()
        return render(request, 'add_contact.html', context={'contact_form': contact_form})

    def post(self, request):
        contact_form = ContactForm(request.POST)
        if not contact_form.is_valid():
            return redirect(reverse(
                'add_contact',
                query_params={'error': ResponseError.INVALID_CONTACT}
            ))

        create_contact(
            request.user,
            name=contact_form.cleaned_data['name'],
            email=contact_form.cleaned_data['email'],
        )
        return redirect('index')


class DeleteContactView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'contacts.delete_contact'

    def post(self, request, pk):
        if not Contact.objects.filter(pk=pk).exists():
            return redirect('index')
        delete_contact(request.user, contact_id=pk)
        return redirect('index')


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect(reverse('sign-in'))


class SignInView(View):
    def get(self, request):
        form = AuthenticationForm()
        error = request.GET.get('error')
        try:
            error = ResponseError[error].value
        except KeyError:
            error = ''
        return render(request, 'sign_in.html', context={
            'sign_in_form': form,
            'error': error,
        })

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if not form.is_valid():
            messages.error(request, 'Invalid username or password')
            return redirect(reverse(
                'sign-in',
                query_params={'error': ResponseError.INVALID_CREDENTIALS.name}
            ))
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, 'Invalid username or password')
            return redirect(reverse(
                'sign-in',
                query_params={'error': ResponseError.INVALID_CREDENTIALS.name}
            ))
        login(request, user)
        return redirect('index')
