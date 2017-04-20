from django import forms
from .models import CustomUser, Ticket
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import IntegrityError
from django_comp.roles import ROLES

class CreateTicketForm(forms.Form):
    title = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)

    def save(self):
        # topic = self.cleaned_data['subject']
        # message = self.cleaned_data['message']
        # sender = self.cleaned_data['sender']
        ticket = Ticket(title=self.cleaned_data['title'],
                        created=timezone.now(),
                        ticketState=Ticket.OPEN_STATUS,
                        message=self.cleaned_data['message'],
                        )
        return ticket

class LoginForm(forms.Form):
    """
       Login Form, works with ajax.
    """

    #login fields
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

    # registration fields
    username_reg = forms.CharField(max_length=100)
    password_reg = forms.CharField(widget=forms.PasswordInput())
    password_again = forms.CharField(widget=forms.PasswordInput())
    role = forms.ChoiceField(choices=ROLES)
class AnswerForm(forms.Form):
    resolution = forms.CharField(widget=forms.Textarea)
    #
    #
    # def get_username(self):
    #     username=self.cleaned_data['username']
    #     return username
    #
    # def get_password(self):
    #     password = self.cleaned_data['password']
    #     return password


    # def save(self):
    #     # topic = self.cleaned_data['subject']
    #     # message = self.cleaned_data['message']
    #     # sender = self.cleaned_data['sender']
    #     ticket = Ticket(title=self.cleaned_data['title'],
    #                     submitter_email=self.cleaned_data['submitter_email'],
    #                     created=timezone.now(),
    #                     status=Ticket.OPEN_STATUS,
    #                     message=self.cleaned_data['message'],
    #                     due_date=self.cleaned_data['due_date'],
    #                     )
    #     return ticket