# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-02-28 15:05
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('easyaudit', '0002_auto_20170125_0759'),
    ]

    operations = [
        migrations.AddField(
            model_name='crudevent',
            name='user_pk_as_string',
            field=models.CharField(blank=True, help_text=b'String version of the user pk', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='crudevent',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
