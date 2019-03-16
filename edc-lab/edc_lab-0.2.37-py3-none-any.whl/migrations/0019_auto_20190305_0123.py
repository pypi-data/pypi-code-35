# Generated by Django 2.1.7 on 2019-03-04 23:23

from django.db import migrations, models
import django_audit_fields.fields.hostname_modification_field
import django_audit_fields.fields.userfield
import django_audit_fields.models.audit_model_mixin


class Migration(migrations.Migration):

    dependencies = [
        ('edc_lab', '0018_auto_20190201_0446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aliquot',
            name='created',
            field=models.DateTimeField(blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow),
        ),
        migrations.AlterField(
            model_name='aliquot',
            name='hostname_modified',
            field=django_audit_fields.fields.hostname_modification_field.HostnameModificationField(blank=True, help_text='System field. (modified on every save)', max_length=50),
        ),
        migrations.AlterField(
            model_name='aliquot',
            name='modified',
            field=models.DateTimeField(blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow),
        ),
        migrations.AlterField(
            model_name='aliquot',
            name='user_created',
            field=django_audit_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user created'),
        ),
        migrations.AlterField(
            model_name='aliquot',
            name='user_modified',
            field=django_audit_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user modified'),
        ),
        migrations.AlterField(
            model_name='box',
            name='created',
            field=models.DateTimeField(blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow),
        ),
        migrations.AlterField(
            model_name='box',
            name='hostname_modified',
            field=django_audit_fields.fields.hostname_modification_field.HostnameModificationField(blank=True, help_text='System field. (modified on every save)', max_length=50),
        ),
        migrations.AlterField(
            model_name='box',
            name='modified',
            field=models.DateTimeField(blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow),
        ),
        migrations.AlterField(
            model_name='box',
            name='user_created',
            field=django_audit_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user created'),
        ),
        migrations.AlterField(
            model_name='box',
            name='user_modified',
            field=django_audit_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user modified'),
        ),
        migrations.AlterField(
            model_name='boxitem',
            name='created',
            field=models.DateTimeField(blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow),
        ),
        migrations.AlterField(
            model_name='boxitem',
            name='hostname_modified',
            field=django_audit_fields.fields.hostname_modification_field.HostnameModificationField(blank=True, help_text='System field. (modified on every save)', max_length=50),
        ),
        migrations.AlterField(
            model_name='boxitem',
            name='modified',
            field=models.DateTimeField(blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow),
        ),
        migrations.AlterField(
            model_name='boxitem',
            name='user_created',
            field=django_audit_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user created'),
        ),
        migrations.AlterField(
            model_name='boxitem',
            name='user_modified',
            field=django_audit_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user modified'),
        ),
        migrations.AlterField(
            model_name='boxtype',
            name='created',
            field=models.DateTimeField(blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow),
        ),
        migrations.AlterField(
            model_name='boxtype',
            name='hostname_modified',
            field=django_audit_fields.fields.hostname_modification_field.HostnameModificationField(blank=True, help_text='System field. (modified on every save)', max_length=50),
        ),
        migrations.AlterField(
            model_name='boxtype',
            name='modified',
            field=models.DateTimeField(blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow),
        ),
        migrations.AlterField(
            model_name='boxtype',
            name='user_created',
            field=django_audit_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user created'),
        ),
        migrations.AlterField(
            model_name='boxtype',
            name='user_modified',
            field=django_audit_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user modified'),
        ),
        migrations.AlterField(
            model_name='consignee',
            name='created',
            field=models.DateTimeField(blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow),
        ),
        migrations.AlterField(
            model_name='consignee',
            name='hostname_modified',
            field=django_audit_fields.fields.hostname_modification_field.HostnameModificationField(blank=True, help_text='System field. (modified on every save)', max_length=50),
        ),
        migrations.AlterField(
            model_name='consignee',
            name='modified',
            field=models.DateTimeField(blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow),
        ),
        migrations.AlterField(
            model_name='consignee',
            name='user_created',
            field=django_audit_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user created'),
        ),
        migrations.AlterField(
            model_name='consignee',
            name='user_modified',
            field=django_audit_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user modified'),
        ),
        migrations.AlterField(
            model_name='historicalaliquot',
            name='created',
            field=models.DateTimeField(blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow),
        ),
        migrations.AlterField(
            model_name='historicalaliquot',
            name='hostname_modified',
            field=django_audit_fields.fields.hostname_modification_field.HostnameModificationField(blank=True, help_text='System field. (modified on every save)', max_length=50),
        ),
        migrations.AlterField(
            model_name='historicalaliquot',
            name='modified',
            field=models.DateTimeField(blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow),
        ),
        migrations.AlterField(
            model_name='historicalaliquot',
            name='user_created',
            field=django_audit_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user created'),
        ),
        migrations.AlterField(
            model_name='historicalaliquot',
            name='user_modified',
            field=django_audit_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user modified'),
        ),
        migrations.AlterField(
            model_name='historicalbox',
            name='created',
            field=models.DateTimeField(blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow),
        ),
        migrations.AlterField(
            model_name='historicalbox',
            name='hostname_modified',
            field=django_audit_fields.fields.hostname_modification_field.HostnameModificationField(blank=True, help_text='System field. (modified on every save)', max_length=50),
        ),
        migrations.AlterField(
            model_name='historicalbox',
            name='modified',
            field=models.DateTimeField(blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow),
        ),
        migrations.AlterField(
            model_name='historicalbox',
            name='user_created',
            field=django_audit_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user created'),
        ),
        migrations.AlterField(
            model_name='historicalbox',
            name='user_modified',
            field=django_audit_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user modified'),
        ),
        migrations.AlterField(
            model_name='historicalboxitem',
            name='created',
            field=models.DateTimeField(blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow),
        ),
        migrations.AlterField(
            model_name='historicalboxitem',
            name='hostname_modified',
            field=django_audit_fields.fields.hostname_modification_field.HostnameModificationField(blank=True, help_text='System field. (modified on every save)', max_length=50),
        ),
        migrations.AlterField(
            model_name='historicalboxitem',
            name='modified',
            field=models.DateTimeField(blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow),
        ),
        migrations.AlterField(
            model_name='historicalboxitem',
            name='user_created',
            field=django_audit_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user created'),
        ),
        migrations.AlterField(
            model_name='historicalboxitem',
            name='user_modified',
            field=django_audit_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user modified'),
        ),
        migrations.AlterField(
            model_name='historicalconsignee',
            name='created',
            field=models.DateTimeField(blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow),
        ),
        migrations.AlterField(
            model_name='historicalconsignee',
            name='hostname_modified',
            field=django_audit_fields.fields.hostname_modification_field.HostnameModificationField(blank=True, help_text='System field. (modified on every save)', max_length=50),
        ),
        migrations.AlterField(
            model_name='historicalconsignee',
            name='modified',
            field=models.DateTimeField(blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow),
        ),
        migrations.AlterField(
            model_name='historicalconsignee',
            name='user_created',
            field=django_audit_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user created'),
        ),
        migrations.AlterField(
            model_name='historicalconsignee',
            name='user_modified',
            field=django_audit_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user modified'),
        ),
        migrations.AlterField(
            model_name='historicalmanifest',
            name='created',
            field=models.DateTimeField(blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow),
        ),
        migrations.AlterField(
            model_name='historicalmanifest',
            name='hostname_modified',
            field=django_audit_fields.fields.hostname_modification_field.HostnameModificationField(blank=True, help_text='System field. (modified on every save)', max_length=50),
        ),
        migrations.AlterField(
            model_name='historicalmanifest',
            name='modified',
            field=models.DateTimeField(blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow),
        ),
        migrations.AlterField(
            model_name='historicalmanifest',
            name='user_created',
            field=django_audit_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user created'),
        ),
        migrations.AlterField(
            model_name='historicalmanifest',
            name='user_modified',
            field=django_audit_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user modified'),
        ),
        migrations.AlterField(
            model_name='historicalorder',
            name='created',
            field=models.DateTimeField(blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow),
        ),
        migrations.AlterField(
            model_name='historicalorder',
            name='hostname_modified',
            field=django_audit_fields.fields.hostname_modification_field.HostnameModificationField(blank=True, help_text='System field. (modified on every save)', max_length=50),
        ),
        migrations.AlterField(
            model_name='historicalorder',
            name='modified',
            field=models.DateTimeField(blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow),
        ),
        migrations.AlterField(
            model_name='historicalorder',
            name='user_created',
            field=django_audit_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user created'),
        ),
        migrations.AlterField(
            model_name='historicalorder',
            name='user_modified',
            field=django_audit_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user modified'),
        ),
        migrations.AlterField(
            model_name='historicalresult',
            name='created',
            field=models.DateTimeField(blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow),
        ),
        migrations.AlterField(
            model_name='historicalresult',
            name='hostname_modified',
            field=django_audit_fields.fields.hostname_modification_field.HostnameModificationField(blank=True, help_text='System field. (modified on every save)', max_length=50),
        ),
        migrations.AlterField(
            model_name='historicalresult',
            name='modified',
            field=models.DateTimeField(blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow),
        ),
        migrations.AlterField(
            model_name='historicalresult',
            name='user_created',
            field=django_audit_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user created'),
        ),
        migrations.AlterField(
            model_name='historicalresult',
            name='user_modified',
            field=django_audit_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user modified'),
        ),
        migrations.AlterField(
            model_name='historicalresultitem',
            name='created',
            field=models.DateTimeField(blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow),
        ),
        migrations.AlterField(
            model_name='historicalresultitem',
            name='hostname_modified',
            field=django_audit_fields.fields.hostname_modification_field.HostnameModificationField(blank=True, help_text='System field. (modified on every save)', max_length=50),
        ),
        migrations.AlterField(
            model_name='historicalresultitem',
            name='modified',
            field=models.DateTimeField(blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow),
        ),
        migrations.AlterField(
            model_name='historicalresultitem',
            name='user_created',
            field=django_audit_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user created'),
        ),
        migrations.AlterField(
            model_name='historicalresultitem',
            name='user_modified',
            field=django_audit_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user modified'),
        ),
        migrations.AlterField(
            model_name='historicalshipper',
            name='created',
            field=models.DateTimeField(blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow),
        ),
        migrations.AlterField(
            model_name='historicalshipper',
            name='hostname_modified',
            field=django_audit_fields.fields.hostname_modification_field.HostnameModificationField(blank=True, help_text='System field. (modified on every save)', max_length=50),
        ),
        migrations.AlterField(
            model_name='historicalshipper',
            name='modified',
            field=models.DateTimeField(blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow),
        ),
        migrations.AlterField(
            model_name='historicalshipper',
            name='user_created',
            field=django_audit_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user created'),
        ),
        migrations.AlterField(
            model_name='historicalshipper',
            name='user_modified',
            field=django_audit_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user modified'),
        ),
        migrations.AlterField(
            model_name='manifest',
            name='created',
            field=models.DateTimeField(blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow),
        ),
        migrations.AlterField(
            model_name='manifest',
            name='hostname_modified',
            field=django_audit_fields.fields.hostname_modification_field.HostnameModificationField(blank=True, help_text='System field. (modified on every save)', max_length=50),
        ),
        migrations.AlterField(
            model_name='manifest',
            name='modified',
            field=models.DateTimeField(blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow),
        ),
        migrations.AlterField(
            model_name='manifest',
            name='user_created',
            field=django_audit_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user created'),
        ),
        migrations.AlterField(
            model_name='manifest',
            name='user_modified',
            field=django_audit_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user modified'),
        ),
        migrations.AlterField(
            model_name='manifestitem',
            name='created',
            field=models.DateTimeField(blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow),
        ),
        migrations.AlterField(
            model_name='manifestitem',
            name='hostname_modified',
            field=django_audit_fields.fields.hostname_modification_field.HostnameModificationField(blank=True, help_text='System field. (modified on every save)', max_length=50),
        ),
        migrations.AlterField(
            model_name='manifestitem',
            name='modified',
            field=models.DateTimeField(blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow),
        ),
        migrations.AlterField(
            model_name='manifestitem',
            name='user_created',
            field=django_audit_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user created'),
        ),
        migrations.AlterField(
            model_name='manifestitem',
            name='user_modified',
            field=django_audit_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user modified'),
        ),
        migrations.AlterField(
            model_name='order',
            name='created',
            field=models.DateTimeField(blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow),
        ),
        migrations.AlterField(
            model_name='order',
            name='hostname_modified',
            field=django_audit_fields.fields.hostname_modification_field.HostnameModificationField(blank=True, help_text='System field. (modified on every save)', max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='modified',
            field=models.DateTimeField(blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow),
        ),
        migrations.AlterField(
            model_name='order',
            name='user_created',
            field=django_audit_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user created'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user_modified',
            field=django_audit_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user modified'),
        ),
        migrations.AlterField(
            model_name='panel',
            name='created',
            field=models.DateTimeField(blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow),
        ),
        migrations.AlterField(
            model_name='panel',
            name='hostname_modified',
            field=django_audit_fields.fields.hostname_modification_field.HostnameModificationField(blank=True, help_text='System field. (modified on every save)', max_length=50),
        ),
        migrations.AlterField(
            model_name='panel',
            name='modified',
            field=models.DateTimeField(blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow),
        ),
        migrations.AlterField(
            model_name='panel',
            name='user_created',
            field=django_audit_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user created'),
        ),
        migrations.AlterField(
            model_name='panel',
            name='user_modified',
            field=django_audit_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user modified'),
        ),
        migrations.AlterField(
            model_name='result',
            name='created',
            field=models.DateTimeField(blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow),
        ),
        migrations.AlterField(
            model_name='result',
            name='hostname_modified',
            field=django_audit_fields.fields.hostname_modification_field.HostnameModificationField(blank=True, help_text='System field. (modified on every save)', max_length=50),
        ),
        migrations.AlterField(
            model_name='result',
            name='modified',
            field=models.DateTimeField(blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow),
        ),
        migrations.AlterField(
            model_name='result',
            name='user_created',
            field=django_audit_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user created'),
        ),
        migrations.AlterField(
            model_name='result',
            name='user_modified',
            field=django_audit_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user modified'),
        ),
        migrations.AlterField(
            model_name='resultitem',
            name='created',
            field=models.DateTimeField(blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow),
        ),
        migrations.AlterField(
            model_name='resultitem',
            name='hostname_modified',
            field=django_audit_fields.fields.hostname_modification_field.HostnameModificationField(blank=True, help_text='System field. (modified on every save)', max_length=50),
        ),
        migrations.AlterField(
            model_name='resultitem',
            name='modified',
            field=models.DateTimeField(blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow),
        ),
        migrations.AlterField(
            model_name='resultitem',
            name='user_created',
            field=django_audit_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user created'),
        ),
        migrations.AlterField(
            model_name='resultitem',
            name='user_modified',
            field=django_audit_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user modified'),
        ),
        migrations.AlterField(
            model_name='shipper',
            name='created',
            field=models.DateTimeField(blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow),
        ),
        migrations.AlterField(
            model_name='shipper',
            name='hostname_modified',
            field=django_audit_fields.fields.hostname_modification_field.HostnameModificationField(blank=True, help_text='System field. (modified on every save)', max_length=50),
        ),
        migrations.AlterField(
            model_name='shipper',
            name='modified',
            field=models.DateTimeField(blank=True, default=django_audit_fields.models.audit_model_mixin.utcnow),
        ),
        migrations.AlterField(
            model_name='shipper',
            name='user_created',
            field=django_audit_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user created'),
        ),
        migrations.AlterField(
            model_name='shipper',
            name='user_modified',
            field=django_audit_fields.fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user modified'),
        ),
    ]
