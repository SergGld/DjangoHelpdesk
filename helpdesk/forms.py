# -*- coding: utf-8 -*-
from django import forms
from .models import Ticket,Categories
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import IntegrityError
from django_comp.roles import ROLES

class CreateTicketForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CreateTicketForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = "Название"
        self.fields['message'].label = "Ваше сообщение"
        self.fields['category'].label = "Категория"

    title = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    category=forms.ModelChoiceField(queryset = Categories.objects.all())
    def save(self):
        ticket = Ticket(title=self.cleaned_data['title'],
                        created=timezone.now(),
                        user=self.user,
                        category=self.cleaned_data['category'],
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
    email = forms.EmailField(widget=forms.EmailInput())
class AnswerForm(forms.Form):
    resolution = forms.CharField(widget=forms.Textarea)
    resolution.label="Ответ"

class RemoveTicketForm(forms.Form):
    CHOICES = [('select1', 'select 1'),
               ('select2', 'select 2')]

    choice = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())