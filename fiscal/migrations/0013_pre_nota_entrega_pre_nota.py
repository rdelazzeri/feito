# Generated by Django 3.2.7 on 2021-12-22 17:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fiscal', '0012_auto_20211222_1403'),
    ]

    operations = [
        migrations.AddField(
            model_name='pre_nota_entrega',
            name='pre_nota',
            field=models.OneToOneField(default=33, on_delete=django.db.models.deletion.CASCADE, related_name='local_entrega', to='fiscal.pre_nota'),
            preserve_default=False,
        ),
    ]