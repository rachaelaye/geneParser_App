# Generated by Django 4.0.5 on 2022-07-08 09:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_transcript_cdsstart_alter_transcript_cdsstop'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transcript',
            name='search_timestamp',
        ),
    ]
