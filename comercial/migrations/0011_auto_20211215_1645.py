# Generated by Django 3.2.7 on 2021-12-15 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comercial', '0010_auto_20211215_1458'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comercial_config',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_ult_orcamento', models.PositiveIntegerField(default='0', verbose_name='Número último orçamento')),
                ('num_ult_pedido', models.PositiveIntegerField(default='0', verbose_name='Número último pedido')),
            ],
        ),
        migrations.AlterField(
            model_name='orcamento',
            name='num_orc',
            field=models.PositiveIntegerField(default=0, verbose_name='Número Orçamento'),
        ),
    ]