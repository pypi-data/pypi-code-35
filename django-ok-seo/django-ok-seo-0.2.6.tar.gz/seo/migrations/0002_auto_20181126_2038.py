from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seo', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='modelinstanceseo',
            name='facebook_app_id',
        ),
        migrations.RemoveField(
            model_name='viewseo',
            name='facebook_app_id',
        ),
        migrations.AddField(
            model_name='modelinstanceseo',
            name='bottom_text',
            field=models.TextField(blank=True, help_text='Can be usefull for some static pages or some objects (like product category).', verbose_name='Page top text for seo'),
        ),
        migrations.AddField(
            model_name='modelinstanceseo',
            name='h1',
            field=models.CharField(blank=True, max_length=255, verbose_name='H1 title'),
        ),
        migrations.AddField(
            model_name='modelinstanceseo',
            name='top_text',
            field=models.TextField(blank=True, help_text='Can be usefull for some static pages or some objects (like product category).', verbose_name='Page top text for seo'),
        ),
        migrations.AddField(
            model_name='viewseo',
            name='bottom_text',
            field=models.TextField(blank=True, help_text='Can be usefull for some static pages or some objects (like product category).', verbose_name='Page top text for seo'),
        ),
        migrations.AddField(
            model_name='viewseo',
            name='h1',
            field=models.CharField(blank=True, max_length=255, verbose_name='H1 title'),
        ),
        migrations.AddField(
            model_name='viewseo',
            name='top_text',
            field=models.TextField(blank=True, help_text='Can be usefull for some static pages or some objects (like product category).', verbose_name='Page top text for seo'),
        ),
    ]
