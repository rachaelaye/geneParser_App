# Generated by Django 4.0.5 on 2022-07-15 11:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_remove_upload_results_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transcript',
            name='upload_id',
        ),
    ]
