# Generated by Django 3.2.7 on 2022-01-17 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comercial', '0025_alter_entrega_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orcamento',
            name='num_orc',
            field=models.PositiveIntegerField(default=0, verbose_name='Número Orçamento'),
        ),
    ]