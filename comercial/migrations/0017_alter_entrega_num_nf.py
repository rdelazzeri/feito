# Generated by Django 3.2.7 on 2021-12-16 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comercial', '0016_alter_entrega_pedido_origem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrega',
            name='num_nf',
            field=models.PositiveIntegerField(default='0', verbose_name='Número da NFe'),
        ),
    ]
