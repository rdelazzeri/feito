# Generated by Django 3.2.7 on 2022-03-25 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entradas', '0014_auto_20220325_0832'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordem_compra_itens',
            name='valor_icms',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=13),
        ),
    ]