# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-13 17:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ResetPasswordToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='When was this token generated')),
                ('key', models.CharField(max_length=64, db_index=True, serialize=False, verbose_name='Key')),
                ('ip_address', models.GenericIPAddressField(default='127.0.0.1', verbose_name='The IP address of this session')),
                ('user_agent', models.CharField(default='', max_length=256, verbose_name='HTTP User Agent')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='password_reset_tokens', to=settings.AUTH_USER_MODEL, verbose_name='The User which is associated to this password reset token')),
            ],
            options={
                'verbose_name_plural': 'Password Reset Tokens',
                'verbose_name': 'Password Reset Token',
            },
        ),
    ]
