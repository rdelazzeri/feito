# Generated by Django 3.2.7 on 2021-12-13 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fiscal', '0002_auto_20211213_1423'),
    ]

    operations = [
        migrations.AddField(
            model_name='nf_config',
            name='aliq_credito_simples',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]
