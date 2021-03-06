# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from helpdesk.forms import CreateTicketForm, LoginForm, AnswerForm,RemoveTicketForm
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
from django.db.models import Q
from django.contrib.auth.decorators import login_required

@login_required(login_url='/helpdesk/')
def user_homepage(request):
    have_resolved_tickets=True;
    user_tickets = Ticket.objects.filter(user=request.user).filter(Q(ticketState=Ticket.OPEN_STATUS) | Q(ticketState=Ticket.REOPENED_STATUS))
    resolved_tickets = Ticket.objects.filter(user=request.user).filter(ticketState=Ticket.RESOLVED_STATUS)
    # ticket=get_object_or_404(Ticket, pk=ticket_id)
    if (resolved_tickets.count()==0):
        have_resolved_tickets=False;

    return render(request, 'helpdesk/user_homepage.html', {
        'user_tickets': user_tickets,
        'resolved_tickets': resolved_tickets,
        'have_resolved_tickets':have_resolved_tickets,
    })

@csrf_protect
@login_required(login_url='/helpdesk/')
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

@login_required(login_url='/helpdesk/')
def ticket_user(request,ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    if request.method == "POST":
        if 'accept' in request.POST:
            ticket.ticketState=Ticket.CLOSED_STATUS
            ticket.save()
            return HttpResponseRedirect(reverse('helpdesk:index'))
        elif 'reject' in request.POST:
            ticket.ticketState = Ticket.REOPENED_STATUS
            ticket.save()
            return HttpResponseRedirect(reverse('helpdesk:index'))

    # if not _has_access_to_queue(request.user, ticket.queue):
    #     raise PermissionDenied()
    return render(request, 'helpdesk/ticket_user.html', {
        'ticket': ticket,
        # 'form': form,
    })

@login_required(login_url='/helpdesk/')
def user_profile(request):
    """
            View for user profile page.
    """
    user=request.user
    try:
        role = get_user_roles(user)[0].name
    except:
        role = 'Администратор'
    if request.method == "POST":
        user.first_name=request.POST.get('first-name','')
        user.profile.phone = request.POST.get('phone-number', '')
        user.username=request.POST.get('login','')
        user.profile.telegram = request.POST.get('telegram', '')
        user.save();
    return render(request, 'helpdesk/user_profile.html', {
        'user': user,
        'role': role,
        # 'form': form,
    })



@login_required(login_url='/helpdesk/')
def removed_ticket(request,ticket_id):
    """
                    View for removing ticket.
    """
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    user=request.user
    if request.method == "POST":
        ticket.delete()
        if 'yes' in request.POST:
            # запись в базу о том что не помогли
            return HttpResponseRedirect(reverse('helpdesk:index'))
        elif 'no' in request.POST:
            # запись в базу о том что не помогли
            return HttpResponseRedirect(reverse('helpdesk:index'))
    return render(request, 'helpdesk/remove_choice_form.html', {

            'ticket': ticket,
        })


@login_required(login_url='/helpdesk/')
def telegram_chat(request):
    return render(request, 'helpdesk/telegram-chat.html', {

    })