# Generated by Django 3.2.7 on 2022-02-03 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0008_movimento_nf_entrada'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movimento',
            name='nf_entrada',
        ),
        migrations.AddField(
            model_name='movimento',
            name='chave',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='movimento',
            name='tipo',
            field=models.CharField(default='', max_length=4),
        ),
    ]
