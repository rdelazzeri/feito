# Generated by Django 3.2.7 on 2022-04-11 21:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('entradas', '0016_auto_20220411_1511'),
    ]

    operations = [
        migrations.AddField(
            model_name='nf_entrada_itens',
            name='obs',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='nf_entrada',
            name='operacao',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='entradas.operacao_entrada'),
        ),
        migrations.AlterField(
            model_name='ordem_compra',
            name='operacao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entradas.operacao_entrada'),
        ),
    ]
