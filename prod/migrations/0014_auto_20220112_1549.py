# Generated by Django 3.2.7 on 2022-01-12 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prod', '0013_auto_20211223_0837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grupo',
            name='desc',
            field=models.CharField(max_length=60, verbose_name='Descrição'),
        ),
        migrations.AlterField(
            model_name='subgrupo',
            name='desc',
            field=models.CharField(max_length=60, verbose_name='Descrição'),
        ),
    ]
