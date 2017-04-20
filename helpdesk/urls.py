from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.login_view, name='login'),
    url(r'^validate_username/$', views.validate_username, name='validate_username'),
    url(r'^index/$', views.base_view, name='index'),
    # url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    # url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^tickets/$', views.ticket_list, name='tickets'),
    url(r'^tickets/(?P<ticket_id>[0-9]+)/$', views.ticket, name='view'),
    # url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^create/$', views.post_new, name='create'),
    # url(r'^login/$', views.login_view, name='login'),
]
