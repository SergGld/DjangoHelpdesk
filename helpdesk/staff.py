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
from django.db.models import Count
from django.core import serializers
import json
from django.core.serializers.json import DjangoJSONEncoder



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
    reopened_tickets=Ticket.objects.filter(staff=request.user).filter(ticketState=Ticket.REOPENED_STATUS)
    latest_ticket_list = Ticket.objects.filter(ticketState=Ticket.OPEN_STATUS).order_by('-created')
    my_ticket = Ticket.objects.filter(staff=request.user).filter(ticketState=Ticket.RESOLVED_STATUS).order_by('-resolved')
    categories=Categories.objects.all()
    # ticket=get_object_or_404(Ticket, pk=ticket_id)
    return render(request, 'helpdesk/tickets.html', {
        'reopened_tickets': reopened_tickets,
        'my_ticket':my_ticket,
        'categories':categories,
        'latest_ticket_list': latest_ticket_list,
    })

def stats_view(request):
    # data=Ticket.objects.values('staff_id').annotate(dcount=Count('staff_id'))
    # print(data)
    data = Ticket.objects.values('ticketState').annotate(y=Count('ticketState'))
    count = Ticket.objects.count()
    # print(data[0]['count'])
    for i in range(len(data)):
        # Ticket.STATUS_CHOICES.__str__(data[i]['ticketState'])
        data[i]['ticketState']={
    1: 'Open',
    2: 'Reopened',
    3: 'Resolved',
    4: 'Closed',
}[ data[i]['ticketState']]
        data[i]['y']=(data[i]['y']/count)*100
    # data['ticket_State'] = data.pop('name')
    data = json.dumps(list(data), cls=DjangoJSONEncoder)
    print(data)
    # json1_data = json.loads(data)

    # print(json1_data)
    return render(request, 'helpdesk/stats.html', {'tickets_data':data})
    # render_template_to_response("helpdesk/stats.html", {"my_data": js_data})

def piestats_view(request):
    # ticket=get_object_or_404(Ticket, pk=ticket_id)
    data=Ticket.objects.values('ticketState').annotate(y=Count('ticketState'))

    print(data)
    return render(request, 'helpdesk/stats.html', {})