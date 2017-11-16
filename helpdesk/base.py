# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from helpdesk.forms import CreateTicketForm, LoginForm, AnswerForm
from helpdesk.models import Ticket,Categories
from django.contrib.auth import authenticate, login
from django.http import Http404
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import JsonResponse
from rolepermissions.roles import assign_role
from rolepermissions.roles import get_user_roles
from django_comp.roles import *
from notify.signals import notify
from django.contrib import auth
from django.views.decorators.csrf import csrf_protect
from datetime import datetime
from django.contrib.auth import get_user_model
from rolepermissions.checkers import has_role
from helpdesk.models import Profile




def validate_username(request):
    """
            View for onchange username_reg, doesn't work.
    """
    username = request.GET.get('username_reg', None)
    data = {
        'is_taken': User.objects.filter(username=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'A user with this username already exists.'
    return JsonResponse(data)


def login_view(request):
    """
        View for login form, works with ajax.
    """
    data={'message':''}
    form = LoginForm()
    if request.method == "POST":
        if 'login' in request.POST:
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password)
            if user is not None:
                    if user.is_active:
                        login(request, user)
                        if has_role(user,"staff"):
                            return HttpResponse('approved_staff', content_type='text/html')
                        if has_role(user,"user"):
                            return HttpResponse('approved_user', content_type='text/html')
                    else:
                        return HttpResponse('Пользователь заблокирован.', content_type='text/html')

            return HttpResponse('Неправильное имя или пароль', content_type='text/html')
        elif 'register' in request.POST:
              print('xd')
              username = request.POST.get('username_reg', '')
              password = request.POST.get('password_reg', '')
              role = request.POST.get('role','')
              email=request.POST.get('email','')
              try:
                    user = get_user_model().objects.create_user(username=username,
                                                  password=password)
                    user.profile.email=email
                    print(role)
                    assign_role(user, role)
                    user.save()
                    return HttpResponse('Cпасибо за регистрацию '+username, content_type='text/html')
                    return user
              except IntegrityError:
                    return HttpResponse('Данный пользователь уже существует.', content_type='text/html')
    return render(request, 'helpdesk/login.html', {'form':form})

def logout(request):
    auth.logout(request)
    # Перенаправление на страницу.
    return HttpResponseRedirect("/helpdesk")