# Generated by Django 3.2.7 on 2021-12-16 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comercial', '0018_entrega_cliente'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrega_item',
            name='pr_tot',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=15, verbose_name='Preço Total.'),
        ),
    ]
