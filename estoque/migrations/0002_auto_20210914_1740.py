# Generated by Django 3.2.7 on 2021-09-14 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estoque',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='criado em'),
        ),
        migrations.AlterField(
            model_name='estoque',
            name='modified',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='modificado em'),
        ),
    ]
