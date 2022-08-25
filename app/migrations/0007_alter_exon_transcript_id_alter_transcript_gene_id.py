# Generated by Django 4.0.5 on 2022-07-08 09:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_transcript_wmrgl_version_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exon',
            name='transcript_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.transcript'),
        ),
        migrations.AlterField(
            model_name='transcript',
            name='gene_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.gene'),
        ),
    ]