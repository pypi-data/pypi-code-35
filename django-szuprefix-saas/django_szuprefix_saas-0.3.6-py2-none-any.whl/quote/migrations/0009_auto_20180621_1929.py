# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-06-21 11:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quote', '0008_auto_20180607_1509'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('manufacturer', 'name'), 'verbose_name': '\u4ea7\u54c1', 'verbose_name_plural': '\u4ea7\u54c1'},
        ),
        migrations.RemoveField(
            model_name='item',
            name='unit',
        ),
        migrations.RemoveField(
            model_name='quote',
            name='unit',
        ),
        migrations.AlterField(
            model_name='request',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, '\u53d6\u6d88'), (1, '\u8be2\u4ef7\u4e2d'), (2, '\u62a5\u4ef7\u4e2d'), (4, '\u5df2\u53d1\u9001\u8be2\u4ef7'), (8, '\u4e2d\u6807'), (16, '\u5931\u6807')], default=1, null=True, verbose_name='\u72b6\u6001'),
        ),
    ]
