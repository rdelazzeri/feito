# Generated by Django 3.2.7 on 2021-12-22 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fiscal', '0010_nfe_transmissao_pre_nota'),
    ]

    operations = [
        migrations.AddField(
            model_name='nfe_transmissao',
            name='nfe',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='nfe_transmissao',
            name='serie',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
    ]