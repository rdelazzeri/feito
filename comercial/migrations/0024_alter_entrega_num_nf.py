# Generated by Django 3.2.7 on 2021-12-21 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comercial', '0023_alter_operacao_classe_imposto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrega',
            name='num_nf',
            field=models.IntegerField(default='0', verbose_name='Número da NFe'),
        ),
    ]