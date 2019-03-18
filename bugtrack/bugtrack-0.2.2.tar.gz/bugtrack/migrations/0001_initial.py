# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-03-04 20:50
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
            name='Bug',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('waiting_for_reply', models.BooleanField(default=False)),
                ('parent', models.CharField(blank=True, default=b'', max_length=8, null=True)),
                ('depends_on', models.CharField(blank=True, default=b'', max_length=256, null=True)),
                ('subject', models.CharField(max_length=256)),
                ('text', models.TextField()),
                ('assigned_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_to', to=settings.AUTH_USER_MODEL)),
                ('executor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='executor', to=settings.AUTH_USER_MODEL)),
                ('tester', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tester', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ManyToManyField(related_name='bug_to_user', to=settings.AUTH_USER_MODEL)),
                ('to_user_ro', models.ManyToManyField(related_name='bug_to_user_ro', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BugEntity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('safe', models.BooleanField(default=False)),
                ('text', models.TextField(blank=True, null=True)),
                ('new_status', models.BooleanField(default=False)),
                ('new_assignment', models.BooleanField(default=False)),
                ('private', models.BooleanField(default=False)),
                ('bug', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bugtrack.Bug')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=256)),
                ('path', models.CharField(max_length=256)),
                ('size', models.IntegerField(default=0)),
                ('description', models.TextField(blank=True, null=True)),
                ('bug_entity', models.ManyToManyField(to='bugtrack.BugEntity')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bugtrack_document_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SavedSearch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=128)),
                ('search_phrase', models.CharField(max_length=1024)),
                ('bgcolor', models.CharField(blank=True, max_length=32, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Switch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=64)),
                ('code', models.CharField(blank=True, max_length=64, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('sorted', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BugStatus',
            fields=[
                ('switch_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='bugtrack.Switch')),
                ('color', models.CharField(blank=True, max_length=16, null=True)),
                ('bgcolor', models.CharField(blank=True, max_length=16, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('bugtrack.switch',),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('switch_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='bugtrack.Switch')),
                ('color', models.CharField(blank=True, max_length=16, null=True)),
                ('parent', models.CharField(blank=True, max_length=16, null=True)),
                ('to_user', models.ManyToManyField(related_name='category_to_user', to=settings.AUTH_USER_MODEL)),
                ('to_user_ro', models.ManyToManyField(related_name='category_to_user_ro', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=('bugtrack.switch',),
        ),
        migrations.CreateModel(
            name='Priority',
            fields=[
                ('switch_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='bugtrack.Switch')),
                ('color', models.CharField(blank=True, max_length=16, null=True)),
                ('is_bold', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=('bugtrack.switch',),
        ),
        migrations.CreateModel(
            name='Severity',
            fields=[
                ('switch_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='bugtrack.Switch')),
                ('color', models.CharField(blank=True, max_length=16, null=True)),
                ('is_bold', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=('bugtrack.switch',),
        ),
        migrations.AddField(
            model_name='bug',
            name='bugstatus',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bugtrack.BugStatus'),
        ),
        migrations.AddField(
            model_name='bug',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bugtrack.Category'),
        ),
        migrations.AddField(
            model_name='bug',
            name='priority',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bugtrack.Priority'),
        ),
        migrations.AddField(
            model_name='bug',
            name='severity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bugtrack.Severity'),
        ),
    ]
