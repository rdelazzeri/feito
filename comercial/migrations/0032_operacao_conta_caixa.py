# Generated by Django 3.2.7 on 2022-01-24 14:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0002_auto_20220124_1104'),
        ('comercial', '0031_auto_20220117_1149'),
    ]

    operations = [
        migrations.AddField(
            model_name='operacao',
            name='conta_caixa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='financeiro.plano_contas'),
        ),
    ]
