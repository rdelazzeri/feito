# Generated by Django 3.2.7 on 2021-12-01 20:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comercial', '0004_auto_20211201_1605'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido_item',
            name='pedido',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='comercial.pedido'),
            preserve_default=False,
        ),
    ]
