# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-16 11:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0003_profile_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='email',
        ),
        migrations.AddField(
            model_name='profile',
            name='phone',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='telegram',
            field=models.TextField(null=True),
        ),
    ]