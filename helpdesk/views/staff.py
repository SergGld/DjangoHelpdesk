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