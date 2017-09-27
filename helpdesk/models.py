# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, UserManager
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime

# Create your models here.
# class Question(models.Model):
#     question_text = models.CharField(max_length=200)
#     pub_date = models.DateTimeField('date published')
#     def __str__(self):
#         return self.question_text
#
#     def was_published_recently(self):
#         return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
#
#
# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)
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



    #Future fields

    #adminId = ""

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     bio = models.TextField(max_length=500, blank=True)
#     location = models.CharField(max_length=30, blank=True)
#     birth_date = models.DateField(null=True, blank=True)
#
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
#

class CustomUser(User):
    """User with app settings."""
    timezone = models.CharField(max_length=50, default='Europe/London')

    # Future fields

    # role =""
    # workplace=""
    # Use UserManager to get the create_user method, etc.
    objects = UserManager()
