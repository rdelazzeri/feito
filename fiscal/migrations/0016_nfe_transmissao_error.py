# Generated by Django 3.2.7 on 2021-12-23 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fiscal', '0015_remove_nfe_transmissao_erro'),
    ]

    operations = [
        migrations.AddField(
            model_name='nfe_transmissao',
            name='error',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]