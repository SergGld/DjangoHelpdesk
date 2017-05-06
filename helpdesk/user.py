from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from helpdesk.forms import CreateTicketForm, LoginForm, AnswerForm
# from .models import Choice, Question
from helpdesk.models import CustomUser, Ticket,Categories
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