# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, UserManager
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime

#Category for ticket
class Categories(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name
    def tickets(self):
        return Ticket.objects.filter(category=self)

class Ticket(models.Model):
    OPEN_STATUS = 1
    REOPENED_STATUS = 2
    RESOLVED_STATUS = 3
    CLOSED_STATUS = 4
    DUPLICATE_STATUS = 5

    STATUS_CHOICES = (
        (OPEN_STATUS, _('Open')),
        (REOPENED_STATUS, _('Reopened')),
        (RESOLVED_STATUS, _('Resolved')),
        (CLOSED_STATUS, _('Closed')),
        (DUPLICATE_STATUS, _('Duplicate')),
    )
    user=models.ForeignKey(settings.AUTH_USER_MODEL)
    staff=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,related_name='resolver')
    category = models.ForeignKey(Categories,null=True,default=0)
    message=models.TextField()
    resolution = models.TextField(null=True)
    created=models.DateTimeField('date published')
    resolved=models.DateTimeField('date published',null=True)
    title = models.TextField(max_length=100)
    ticketState = models.IntegerField(
        _('Status'),
        choices=STATUS_CHOICES,
        default=OPEN_STATUS,
    )
    def __str__(self):
        return self.title

#extended User profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.TextField(null=True)
    telegram = models.TextField(null=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

# def get_fullname(self):
#     return se


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


