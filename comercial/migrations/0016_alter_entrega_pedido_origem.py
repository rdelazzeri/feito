# Generated by Django 3.2.7 on 2021-12-16 20:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comercial', '0015_auto_20211216_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrega',
            name='pedido_origem',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='entregas', to='comercial.pedido'),
        ),
    ]
