# Generated by Django 3.2.7 on 2022-01-25 11:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('fiscal', '0016_nfe_transmissao_error'),
    ]

    operations = [
        migrations.AddField(
            model_name='pre_nota',
            name='data_emissao',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
