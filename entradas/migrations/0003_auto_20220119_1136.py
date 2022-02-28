# Generated by Django 3.2.7 on 2022-01-19 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entradas', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='nf_entrada',
            name='num_oc',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='nf_entrada',
            name='serie',
            field=models.PositiveSmallIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='nf_entrada',
            name='tipo_frete',
            field=models.CharField(choices=[('1', 'CIF'), ('2', 'FOB')], default='2', max_length=1),
        ),
    ]
