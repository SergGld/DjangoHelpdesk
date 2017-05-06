from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from .forms import CreateTicketForm, LoginForm, AnswerForm
# from .models import Choice, Question
from .models import CustomUser, Ticket,Categories
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
                        return HttpResponse('approved', content_type='text/html')
                    else:
                        return HttpResponse('Пользователь заблокирован.', content_type='text/html')

            return HttpResponse('Неправильное имя или пароль', content_type='text/html')
        elif 'register' in request.POST:
              print('xd')
              username = request.POST.get('username_reg', '')
              password = request.POST.get('password_reg', '')
              role = request.POST.get('role','')
              try:
                    user = get_user_model().objects.create_user(username=username,
                                                  password=password)
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
def user_homepage(request):
    user_tickets = Ticket.objects.filter(user=request.user).filter(ticketState=Ticket.OPEN_STATUS)
    resolved_tickets = Ticket.objects.filter(user=request.user).filter(ticketState=Ticket.RESOLVED_STATUS)
    # ticket=get_object_or_404(Ticket, pk=ticket_id)
    return render(request, 'helpdesk/user_homepage.html', {
        'user_tickets': user_tickets,
        'resolved_tickets': resolved_tickets,
    })

@csrf_protect
def post_new(request):
    categories=Categories.objects.all()
    # if 'ajax' in request.POST:
    if request.method == "POST":

        form = CreateTicketForm(request.POST,user=request.user)
        if form.is_valid():
            post = form.save()
            post.user=request.user
            post.save()
            # return HttpResponseRedirect("/helpdesk/index")
            classname='3';
            return HttpResponseRedirect(reverse('helpdesk:index'))
            # return render(request, 'helpdesk/user_homepage.html', {'user_message': 'Ваша заявка передана на рассмотрение.'})
            # return HttpResponse('Ваша заявка передана на рассмотрение', content_type='text/html')
    else:
        form = CreateTicketForm()
    return render(request, 'helpdesk/create_ticket.html', {'form': form,'categories':categories})

def ticket_list(request):
    latest_ticket_list = Ticket.objects.filter(ticketState=Ticket.OPEN_STATUS).order_by('-created')
    my_ticket = Ticket.objects.filter(staff=request.user).filter(ticketState=Ticket.RESOLVED_STATUS).order_by('-resolved')
    categories=Categories.objects.all()
    # ticket=get_object_or_404(Ticket, pk=ticket_id)
    return render(request, 'helpdesk/tickets.html', {
        'my_ticket':my_ticket,
        'categories':categories,
        'latest_ticket_list': latest_ticket_list,
    })

def ticket(request,ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    form = AnswerForm()
    if request.method == "POST":
        resolution = request.POST.get('resolution', '')
        ticket.resolution=resolution
        ticket.ticketState = Ticket.RESOLVED_STATUS
        ticket.staff=request.user
        ticket.resolved=datetime.now()
        ticket.save()
        notify.send(request.user, recipient=ticket.user, actor=request.user,
        verb = 'followed you.', nf_type = 'followed_by_one_user')
        return HttpResponseRedirect(reverse('helpdesk:tickets'))
    # if not _has_access_to_queue(request.user, ticket.queue):
    #     raise PermissionDenied()
    return render(request, 'helpdesk/ticket_staff.html', {
        'ticket': ticket,
        'form': form,
        # 'form': form,
    })
def ticket_user(request,ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)

    # if not _has_access_to_queue(request.user, ticket.queue):
    #     raise PermissionDenied()
    return render(request, 'helpdesk/ticket_user.html', {
        'ticket': ticket,
        # 'form': form,
    })
def user_profile(request):
    """
            View for user profile page.
    """
    user=request.user
    try:
        role = get_user_roles(user)[0].name
    except:
        role = 'Администратор'
    return render(request, 'helpdesk/user_profile.html', {
        'username': user,
        'role': role,
        # 'form': form,
    })

def thanks(request):
    return render(request, 'helpdesk/thanks.html', {
        'ticket': ticket,
        # 'form': form,
    })



