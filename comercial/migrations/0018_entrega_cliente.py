# Generated by Django 3.2.7 on 2021-12-16 20:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cadastro', '0004_parceiro_suframa'),
        ('comercial', '0017_alter_entrega_num_nf'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrega',
            name='cliente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='entregas', to='cadastro.parceiro'),
        ),
    ]