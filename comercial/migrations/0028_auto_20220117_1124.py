# Generated by Django 3.2.7 on 2022-01-17 14:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comercial', '0027_auto_20220117_1106'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orcamento',
            name='cliente',
        ),
        migrations.RemoveField(
            model_name='orcamento',
            name='data_cadastro',
        ),
        migrations.RemoveField(
            model_name='orcamento',
            name='data_previsao',
        ),
        migrations.RemoveField(
            model_name='orcamento',
            name='num_orc_cli',
        ),
        migrations.RemoveField(
            model_name='orcamento',
            name='obs',
        ),
        migrations.RemoveField(
            model_name='orcamento',
            name='operacao',
        ),
        migrations.RemoveField(
            model_name='orcamento',
            name='origem',
        ),
        migrations.RemoveField(
            model_name='orcamento',
            name='previsao_entrega',
        ),
        migrations.RemoveField(
            model_name='orcamento',
            name='status',
        ),
        migrations.RemoveField(
            model_name='orcamento',
            name='tipo_frete',
        ),
        migrations.RemoveField(
            model_name='orcamento',
            name='transportadora',
        ),
        migrations.RemoveField(
            model_name='orcamento',
            name='validade_orcamento',
        ),
        migrations.RemoveField(
            model_name='orcamento',
            name='valor_frete',
        ),
        migrations.RemoveField(
            model_name='orcamento',
            name='valor_total_orcamento',
        ),
        migrations.RemoveField(
            model_name='orcamento',
            name='valor_total_produtos',
        ),
        migrations.RemoveField(
            model_name='orcamento',
            name='vencimentos',
        ),
    ]
