# Generated by Django 3.2.7 on 2022-02-07 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0011_auto_20220203_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimento',
            name='desc',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]