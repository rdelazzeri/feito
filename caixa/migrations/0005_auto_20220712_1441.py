# Generated by Django 3.2.7 on 2022-07-12 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caixa', '0004_rename_bancoo_cc_banco'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cc',
            name='banco',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='cc',
            name='desc',
            field=models.CharField(max_length=80),
        ),
        migrations.AlterField(
            model_name='conta',
            name='conta',
            field=models.CharField(max_length=80),
        ),
    ]
