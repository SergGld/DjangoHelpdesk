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
from django_comp.roles import *
from notify.signals import notify
from django.contrib import auth
from django.views.decorators.csrf import csrf_protect

# Create your views here.
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'helpdesk/login.html', context)
#
# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'helpdesk/detail.html', {'question': question})
#
# def results(request, question_id):
#     response = "You're looking at the results of question %s."
#     return HttpResponse(response % question_id)

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
              username = request.POST.get('username_reg', '')
              password = request.POST.get('password_reg', '')
              role = request.POST.get('role','')
              try:
                    user = User.objects.create_user(username=username,
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
def base_view(request):
    return render(request, 'helpdesk/user_homepage.html', {})

@csrf_protect
def post_new(request):
    categories=Categories.objects.all()
    # if 'ajax' in request.POST:
    if request.method == "POST":
        if request.is_ajax():
            cat=request.POST.get('cat', '')
            category=Categories.objects.get(pk=cat)
        form = CreateTicketForm(request.POST,user=request.user,category=category)
        if form.is_valid():
            post = form.save()
            post.user=request.user
            post.save()
            return render(request, 'helpdesk/create_ticket.html', {'form': form})
    else:
        form = CreateTicketForm()
    return render(request, 'helpdesk/create_ticket.html', {'form': form,'categories':categories})

def ticket_list(request):
    latest_ticket_list = Ticket.objects.order_by('-created')[:5]
    # ticket=get_object_or_404(Ticket, pk=ticket_id)
    return render(request, 'helpdesk/tickets.html', {
        'latest_ticket_list': latest_ticket_list,
        'error_message': "You didn't select a choice.",
    })

def ticket(request,ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    form = AnswerForm()
    if request.method == "POST":
        resolution = request.POST.get('resolution', '')
        ticket.resolution=resolution
        ticket.ticketState = Ticket.RESOLVED_STATUS
        ticket.save()
        notify.send(request.user, recipient=ticket.user, actor=request.user,
        verb = 'followed you.', nf_type = 'followed_by_one_user')
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
def user_profile():
    """
            View for user profile page.
    """
    return;


# def index(request):
#     some="";
#     return render(request, 'helpdesk/login.html', {
#         'some': some,
#         'error_message': "You didn't select a choice.",
#     })
# class TicketsView(generic.ListView):
#     template_name = 'helpdesk/tickets.html'
#     context_object_name = 'latest_ticket_list'
#
#     def get_queryset(self):
#         """Return the last five published questions."""
#         return Ticket.objects.order_by('-created')[:5]
#
#


# class IndexView(generic.ListView):
#     template_name = 'helpdesk/login.html'
#     context_object_name = 'latest_question_list'
#
#     def get_queryset(self):
#         """Return the last five published questions."""
#         return Question.objects.order_by('-pub_date')[:5]
#
#
# class DetailView(generic.DetailView):
#     model = Question
#     template_name = 'helpdesk/detail.html'
#
#
# class ResultsView(generic.DetailView):
#     model = Question
#     template_name = 'helpdesk/ticket_staff.html'
#
#
#
# def vote(request, question_id):
#     return HttpResponse("You're voting on question %s." % question_id)
#
# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(request, 'helpdesk/detail.html', {
#             'question': question,
#             'error_message': "You didn't select a choice.",
#         })
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse('helpdesk:results', args=(question.id,)))
#
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'helpdesk/ticket_staff.html', {'question': question})


