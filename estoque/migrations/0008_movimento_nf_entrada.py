# Generated by Django 3.2.7 on 2022-02-02 20:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('entradas', '0008_remove_nf_entrada_itens_mov_estoque'),
        ('estoque', '0007_movimento'),
    ]

    operations = [
        migrations.AddField(
            model_name='movimento',
            name='nf_entrada',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='entradas.nf_entrada_itens'),
        ),
    ]
