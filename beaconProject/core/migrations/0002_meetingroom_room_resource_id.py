# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-07-28 19:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='meetingroom',
            name='room_resource_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]