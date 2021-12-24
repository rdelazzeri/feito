# Generated by Django 3.2.7 on 2021-12-22 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fiscal', '0013_pre_nota_entrega_pre_nota'),
    ]

    operations = [
        migrations.AddField(
            model_name='nfe_transmissao',
            name='erro',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='nfe_transmissao',
            name='danfe',
            field=models.URLField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='nfe_transmissao',
            name='danfe_simples',
            field=models.URLField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='nfe_transmissao',
            name='log',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='nfe_transmissao',
            name='xml',
            field=models.URLField(blank=True, max_length=300, null=True),
        ),
    ]
