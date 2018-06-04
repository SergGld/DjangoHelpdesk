# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import base,staff,user


#base views urls
urlpatterns = [
    url(r'^$', base.login_view, name='login'),
    url(r'^logout/$', base.logout, name='logout'),
    url(r'^telegram/$', base.test_telegram, name='login'),
]

#user views urls
urlpatterns +=[
    url(r'^index/$', user.user_homepage, name='index'),
    url(r'^index/(?P<ticket_id>[0-9]+)/$',user.ticket_user, name='view'),
    url(r'^profile/$', user.user_profile, name='profile'),
    url(r'^create/$', user.post_new, name='create'),
    url(r'^index/remove/(?P<ticket_id>[0-9]+)$', user.removed_ticket, name='remove'),
    url(r'^index/chat/$', user.telegram_chat, name='chat'),
]

#staff views urls
urlpatterns +=[
    url(r'^tickets/category/(?P<category_id>[0-9]+)/$', staff.category_view, name='category'),
    url(r'^tickets/$', staff.ticket_list, name='tickets'),
    url(r'^tickets/(?P<ticket_id>[0-9]+)/$', staff.ticket, name='view'),
    url(r'^stats/$', staff.stats_view, name='stats'),

]