# Generated by Django 3.2.7 on 2022-04-05 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comercial', '0034_alter_entrega_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='num_oc_cli',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Número Cliente'),
        ),
    ]
