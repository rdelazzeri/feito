# Generated by Django 3.2.7 on 2022-07-12 16:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('caixa', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cc',
            name='conta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='caixa.conta'),
        ),
    ]
