# Generated by Django 2.1 on 2018-10-06 22:53

from django.db import migrations, models
import django.db.models.deletion
import edc_sites.models
import edc_locator.model_mixins.locator_model_mixin


class Migration(migrations.Migration):

    dependencies = [
        ("edc_action_item", "0011_auto_20181009_2236"),
        ("edc_locator", "0010_auto_20180809_0301"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="subjectlocator",
            managers=[
                ("on_site", edc_sites.models.CurrentSiteManager()),
                (
                    "objects",
                    edc_locator.model_mixins.locator_model_mixin.LocatorManager(),
                ),
            ],
        ),
        migrations.RenameField(
            model_name="historicalsubjectlocator",
            old_name="parent_reference_identifier",
            new_name="parent_action_identifier",
        ),
        migrations.RenameField(
            model_name="historicalsubjectlocator",
            old_name="related_reference_identifier",
            new_name="related_action_identifier",
        ),
        migrations.RenameField(
            model_name="subjectlocator",
            old_name="parent_reference_identifier",
            new_name="parent_action_identifier",
        ),
        migrations.RenameField(
            model_name="subjectlocator",
            old_name="related_reference_identifier",
            new_name="related_action_identifier",
        ),
        migrations.AddField(
            model_name="historicalsubjectlocator",
            name="action_item",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="edc_action_item.ActionItem",
            ),
        ),
        migrations.AddField(
            model_name="subjectlocator",
            name="action_item",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="edc_action_item.ActionItem",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectlocator",
            name="action_identifier",
            field=models.CharField(null=True, max_length=50),
        ),
        migrations.AlterField(
            model_name="subjectlocator",
            name="action_identifier",
            field=models.CharField(max_length=50, null=True),
        ),
    ]
