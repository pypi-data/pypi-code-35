# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-21 07:19
from __future__ import unicode_literals

import _socket
from django.db import migrations, models
import django_revision.revision_field
import edc_model_fields.fields.hostname_modification_field
import edc_model_fields.fields.userfield
import edc_model_fields.fields.uuid_auto_field
import edc_utils


class Migration(migrations.Migration):

    dependencies = [("edc_lab", "0007_auto_20170321_1119")]

    operations = [
        migrations.CreateModel(
            name="IdentifierHistory",
            fields=[
                (
                    "created",
                    models.DateTimeField(blank=True, default=edc_utils.date.get_utcnow),
                ),
                (
                    "modified",
                    models.DateTimeField(blank=True, default=edc_utils.date.get_utcnow),
                ),
                (
                    "user_created",
                    edc_model_fields.fields.userfield.UserField(
                        blank=True,
                        help_text="Updated by admin.save_model",
                        max_length=50,
                        verbose_name="user created",
                    ),
                ),
                (
                    "user_modified",
                    edc_model_fields.fields.userfield.UserField(
                        blank=True,
                        help_text="Updated by admin.save_model",
                        max_length=50,
                        verbose_name="user modified",
                    ),
                ),
                (
                    "hostname_created",
                    models.CharField(
                        blank=True,
                        default=_socket.gethostname,
                        help_text="System field. (modified on create only)",
                        max_length=60,
                    ),
                ),
                (
                    "hostname_modified",
                    edc_model_fields.fields.hostname_modification_field.HostnameModificationField(
                        blank=True,
                        help_text="System field. (modified on every save)",
                        max_length=50,
                    ),
                ),
                (
                    "revision",
                    django_revision.revision_field.RevisionField(
                        blank=True,
                        editable=False,
                        help_text="System field. Git repository tag:branch:commit.",
                        max_length=75,
                        null=True,
                        verbose_name="Revision",
                    ),
                ),
                ("device_created", models.CharField(blank=True, max_length=10)),
                ("device_modified", models.CharField(blank=True, max_length=10)),
                (
                    "id",
                    edc_model_fields.fields.uuid_auto_field.UUIDAutoField(
                        blank=True,
                        editable=False,
                        help_text="System auto field. UUID primary key.",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("identifier", models.CharField(max_length=50, unique=True)),
                ("identifier_type", models.CharField(max_length=50)),
                ("identifier_prefix", models.CharField(max_length=25, null=True)),
            ],
            options={"abstract": False},
        ),
        migrations.AddField(
            model_name="aliquot",
            name="device_created",
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name="aliquot",
            name="device_modified",
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name="box",
            name="device_created",
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name="box",
            name="device_modified",
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name="boxitem",
            name="device_created",
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name="boxitem",
            name="device_modified",
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name="boxtype",
            name="device_created",
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name="boxtype",
            name="device_modified",
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name="consignee",
            name="device_created",
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name="consignee",
            name="device_modified",
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name="historicalaliquot",
            name="device_created",
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name="historicalaliquot",
            name="device_modified",
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name="historicalaliquot",
            name="history_change_reason",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="historicalbox",
            name="device_created",
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name="historicalbox",
            name="device_modified",
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name="historicalbox",
            name="history_change_reason",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="historicalboxitem",
            name="device_created",
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name="historicalboxitem",
            name="device_modified",
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name="historicalboxitem",
            name="history_change_reason",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="historicalconsignee",
            name="device_created",
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name="historicalconsignee",
            name="device_modified",
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name="historicalconsignee",
            name="history_change_reason",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="historicalmanifest",
            name="device_created",
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name="historicalmanifest",
            name="device_modified",
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name="historicalmanifest",
            name="history_change_reason",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="historicalshipper",
            name="device_created",
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name="historicalshipper",
            name="device_modified",
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name="historicalshipper",
            name="history_change_reason",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="manifest",
            name="device_created",
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name="manifest",
            name="device_modified",
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name="manifestitem",
            name="device_created",
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name="manifestitem",
            name="device_modified",
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name="shipper",
            name="device_created",
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name="shipper",
            name="device_modified",
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name="aliquot",
            name="hostname_created",
            field=models.CharField(
                blank=True,
                default=_socket.gethostname,
                help_text="System field. (modified on create only)",
                max_length=60,
            ),
        ),
        migrations.AlterField(
            model_name="aliquot",
            name="slug",
            field=models.CharField(
                db_index=True,
                default="",
                editable=False,
                help_text="a field used for quick search",
                max_length=250,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="aliquot",
            name="user_created",
            field=edc_model_fields.fields.userfield.UserField(
                blank=True,
                help_text="Updated by admin.save_model",
                max_length=50,
                verbose_name="user created",
            ),
        ),
        migrations.AlterField(
            model_name="aliquot",
            name="user_modified",
            field=edc_model_fields.fields.userfield.UserField(
                blank=True,
                help_text="Updated by admin.save_model",
                max_length=50,
                verbose_name="user modified",
            ),
        ),
        migrations.AlterField(
            model_name="box",
            name="hostname_created",
            field=models.CharField(
                blank=True,
                default=_socket.gethostname,
                help_text="System field. (modified on create only)",
                max_length=60,
            ),
        ),
        migrations.AlterField(
            model_name="box",
            name="slug",
            field=models.CharField(
                db_index=True,
                default="",
                editable=False,
                help_text="a field used for quick search",
                max_length=250,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="box",
            name="user_created",
            field=edc_model_fields.fields.userfield.UserField(
                blank=True,
                help_text="Updated by admin.save_model",
                max_length=50,
                verbose_name="user created",
            ),
        ),
        migrations.AlterField(
            model_name="box",
            name="user_modified",
            field=edc_model_fields.fields.userfield.UserField(
                blank=True,
                help_text="Updated by admin.save_model",
                max_length=50,
                verbose_name="user modified",
            ),
        ),
        migrations.AlterField(
            model_name="boxitem",
            name="hostname_created",
            field=models.CharField(
                blank=True,
                default=_socket.gethostname,
                help_text="System field. (modified on create only)",
                max_length=60,
            ),
        ),
        migrations.AlterField(
            model_name="boxitem",
            name="slug",
            field=models.CharField(
                db_index=True,
                default="",
                editable=False,
                help_text="a field used for quick search",
                max_length=250,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="boxitem",
            name="user_created",
            field=edc_model_fields.fields.userfield.UserField(
                blank=True,
                help_text="Updated by admin.save_model",
                max_length=50,
                verbose_name="user created",
            ),
        ),
        migrations.AlterField(
            model_name="boxitem",
            name="user_modified",
            field=edc_model_fields.fields.userfield.UserField(
                blank=True,
                help_text="Updated by admin.save_model",
                max_length=50,
                verbose_name="user modified",
            ),
        ),
        migrations.AlterField(
            model_name="boxtype",
            name="hostname_created",
            field=models.CharField(
                blank=True,
                default=_socket.gethostname,
                help_text="System field. (modified on create only)",
                max_length=60,
            ),
        ),
        migrations.AlterField(
            model_name="boxtype",
            name="user_created",
            field=edc_model_fields.fields.userfield.UserField(
                blank=True,
                help_text="Updated by admin.save_model",
                max_length=50,
                verbose_name="user created",
            ),
        ),
        migrations.AlterField(
            model_name="boxtype",
            name="user_modified",
            field=edc_model_fields.fields.userfield.UserField(
                blank=True,
                help_text="Updated by admin.save_model",
                max_length=50,
                verbose_name="user modified",
            ),
        ),
        migrations.AlterField(
            model_name="consignee",
            name="hostname_created",
            field=models.CharField(
                blank=True,
                default=_socket.gethostname,
                help_text="System field. (modified on create only)",
                max_length=60,
            ),
        ),
        migrations.AlterField(
            model_name="consignee",
            name="user_created",
            field=edc_model_fields.fields.userfield.UserField(
                blank=True,
                help_text="Updated by admin.save_model",
                max_length=50,
                verbose_name="user created",
            ),
        ),
        migrations.AlterField(
            model_name="consignee",
            name="user_modified",
            field=edc_model_fields.fields.userfield.UserField(
                blank=True,
                help_text="Updated by admin.save_model",
                max_length=50,
                verbose_name="user modified",
            ),
        ),
        migrations.AlterField(
            model_name="historicalaliquot",
            name="hostname_created",
            field=models.CharField(
                blank=True,
                default=_socket.gethostname,
                help_text="System field. (modified on create only)",
                max_length=60,
            ),
        ),
        migrations.AlterField(
            model_name="historicalaliquot",
            name="slug",
            field=models.CharField(
                db_index=True,
                default="",
                editable=False,
                help_text="a field used for quick search",
                max_length=250,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="historicalaliquot",
            name="user_created",
            field=edc_model_fields.fields.userfield.UserField(
                blank=True,
                help_text="Updated by admin.save_model",
                max_length=50,
                verbose_name="user created",
            ),
        ),
        migrations.AlterField(
            model_name="historicalaliquot",
            name="user_modified",
            field=edc_model_fields.fields.userfield.UserField(
                blank=True,
                help_text="Updated by admin.save_model",
                max_length=50,
                verbose_name="user modified",
            ),
        ),
        migrations.AlterField(
            model_name="historicalbox",
            name="hostname_created",
            field=models.CharField(
                blank=True,
                default=_socket.gethostname,
                help_text="System field. (modified on create only)",
                max_length=60,
            ),
        ),
        migrations.AlterField(
            model_name="historicalbox",
            name="slug",
            field=models.CharField(
                db_index=True,
                default="",
                editable=False,
                help_text="a field used for quick search",
                max_length=250,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="historicalbox",
            name="user_created",
            field=edc_model_fields.fields.userfield.UserField(
                blank=True,
                help_text="Updated by admin.save_model",
                max_length=50,
                verbose_name="user created",
            ),
        ),
        migrations.AlterField(
            model_name="historicalbox",
            name="user_modified",
            field=edc_model_fields.fields.userfield.UserField(
                blank=True,
                help_text="Updated by admin.save_model",
                max_length=50,
                verbose_name="user modified",
            ),
        ),
        migrations.AlterField(
            model_name="historicalboxitem",
            name="hostname_created",
            field=models.CharField(
                blank=True,
                default=_socket.gethostname,
                help_text="System field. (modified on create only)",
                max_length=60,
            ),
        ),
        migrations.AlterField(
            model_name="historicalboxitem",
            name="slug",
            field=models.CharField(
                db_index=True,
                default="",
                editable=False,
                help_text="a field used for quick search",
                max_length=250,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="historicalboxitem",
            name="user_created",
            field=edc_model_fields.fields.userfield.UserField(
                blank=True,
                help_text="Updated by admin.save_model",
                max_length=50,
                verbose_name="user created",
            ),
        ),
        migrations.AlterField(
            model_name="historicalboxitem",
            name="user_modified",
            field=edc_model_fields.fields.userfield.UserField(
                blank=True,
                help_text="Updated by admin.save_model",
                max_length=50,
                verbose_name="user modified",
            ),
        ),
        migrations.AlterField(
            model_name="historicalconsignee",
            name="hostname_created",
            field=models.CharField(
                blank=True,
                default=_socket.gethostname,
                help_text="System field. (modified on create only)",
                max_length=60,
            ),
        ),
        migrations.AlterField(
            model_name="historicalconsignee",
            name="user_created",
            field=edc_model_fields.fields.userfield.UserField(
                blank=True,
                help_text="Updated by admin.save_model",
                max_length=50,
                verbose_name="user created",
            ),
        ),
        migrations.AlterField(
            model_name="historicalconsignee",
            name="user_modified",
            field=edc_model_fields.fields.userfield.UserField(
                blank=True,
                help_text="Updated by admin.save_model",
                max_length=50,
                verbose_name="user modified",
            ),
        ),
        migrations.AlterField(
            model_name="historicalmanifest",
            name="hostname_created",
            field=models.CharField(
                blank=True,
                default=_socket.gethostname,
                help_text="System field. (modified on create only)",
                max_length=60,
            ),
        ),
        migrations.AlterField(
            model_name="historicalmanifest",
            name="slug",
            field=models.CharField(
                db_index=True,
                default="",
                editable=False,
                help_text="a field used for quick search",
                max_length=250,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="historicalmanifest",
            name="user_created",
            field=edc_model_fields.fields.userfield.UserField(
                blank=True,
                help_text="Updated by admin.save_model",
                max_length=50,
                verbose_name="user created",
            ),
        ),
        migrations.AlterField(
            model_name="historicalmanifest",
            name="user_modified",
            field=edc_model_fields.fields.userfield.UserField(
                blank=True,
                help_text="Updated by admin.save_model",
                max_length=50,
                verbose_name="user modified",
            ),
        ),
        migrations.AlterField(
            model_name="historicalshipper",
            name="hostname_created",
            field=models.CharField(
                blank=True,
                default=_socket.gethostname,
                help_text="System field. (modified on create only)",
                max_length=60,
            ),
        ),
        migrations.AlterField(
            model_name="historicalshipper",
            name="user_created",
            field=edc_model_fields.fields.userfield.UserField(
                blank=True,
                help_text="Updated by admin.save_model",
                max_length=50,
                verbose_name="user created",
            ),
        ),
        migrations.AlterField(
            model_name="historicalshipper",
            name="user_modified",
            field=edc_model_fields.fields.userfield.UserField(
                blank=True,
                help_text="Updated by admin.save_model",
                max_length=50,
                verbose_name="user modified",
            ),
        ),
        migrations.AlterField(
            model_name="manifest",
            name="hostname_created",
            field=models.CharField(
                blank=True,
                default=_socket.gethostname,
                help_text="System field. (modified on create only)",
                max_length=60,
            ),
        ),
        migrations.AlterField(
            model_name="manifest",
            name="slug",
            field=models.CharField(
                db_index=True,
                default="",
                editable=False,
                help_text="a field used for quick search",
                max_length=250,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="manifest",
            name="user_created",
            field=edc_model_fields.fields.userfield.UserField(
                blank=True,
                help_text="Updated by admin.save_model",
                max_length=50,
                verbose_name="user created",
            ),
        ),
        migrations.AlterField(
            model_name="manifest",
            name="user_modified",
            field=edc_model_fields.fields.userfield.UserField(
                blank=True,
                help_text="Updated by admin.save_model",
                max_length=50,
                verbose_name="user modified",
            ),
        ),
        migrations.AlterField(
            model_name="manifestitem",
            name="hostname_created",
            field=models.CharField(
                blank=True,
                default=_socket.gethostname,
                help_text="System field. (modified on create only)",
                max_length=60,
            ),
        ),
        migrations.AlterField(
            model_name="manifestitem",
            name="slug",
            field=models.CharField(
                db_index=True,
                default="",
                editable=False,
                help_text="a field used for quick search",
                max_length=250,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="manifestitem",
            name="user_created",
            field=edc_model_fields.fields.userfield.UserField(
                blank=True,
                help_text="Updated by admin.save_model",
                max_length=50,
                verbose_name="user created",
            ),
        ),
        migrations.AlterField(
            model_name="manifestitem",
            name="user_modified",
            field=edc_model_fields.fields.userfield.UserField(
                blank=True,
                help_text="Updated by admin.save_model",
                max_length=50,
                verbose_name="user modified",
            ),
        ),
        migrations.AlterField(
            model_name="shipper",
            name="hostname_created",
            field=models.CharField(
                blank=True,
                default=_socket.gethostname,
                help_text="System field. (modified on create only)",
                max_length=60,
            ),
        ),
        migrations.AlterField(
            model_name="shipper",
            name="user_created",
            field=edc_model_fields.fields.userfield.UserField(
                blank=True,
                help_text="Updated by admin.save_model",
                max_length=50,
                verbose_name="user created",
            ),
        ),
        migrations.AlterField(
            model_name="shipper",
            name="user_modified",
            field=edc_model_fields.fields.userfield.UserField(
                blank=True,
                help_text="Updated by admin.save_model",
                max_length=50,
                verbose_name="user modified",
            ),
        ),
    ]
