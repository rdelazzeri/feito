# Generated by Django 3.2.7 on 2021-12-09 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comercial', '0005_pedido_item_pedido'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido_item',
            name='qtd_entregue',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=15, verbose_name='Qtd Entregue'),
        ),
        migrations.AddField(
            model_name='pedido_item',
            name='saldo',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=15, verbose_name='Saldo'),
        ),
        migrations.AddField(
            model_name='pedido_item',
            name='val_entregue',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=15, verbose_name='Valor faturado'),
        ),
    ]