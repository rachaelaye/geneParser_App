# Generated by Django 4.0.5 on 2022-07-08 09:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_remove_transcript_search_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transcript',
            name='wmrgl_version_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.wmrglversion'),
        ),
    ]
