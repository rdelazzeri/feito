# Generated by Django 3.2.7 on 2021-12-14 19:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('prod', '0010_alter_prod_cod'),
        ('cadastro', '0004_parceiro_suframa'),
        ('comercial', '0007_auto_20211213_1423'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entrega',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.PositiveIntegerField(default='0', unique=True, verbose_name='Número')),
                ('num_nf', models.PositiveIntegerField(default='0', unique=True, verbose_name='Número da NFe')),
                ('status', models.PositiveIntegerField(choices=[(0, 'RASCUNHO'), (1, 'CONCLUÍDA')], default=0)),
                ('data_cadastro', models.DateTimeField(auto_now_add=True, null=True)),
                ('data_emissao', models.DateTimeField(blank=True, null=True)),
                ('tipo_frete', models.CharField(choices=[('1', 'CIF'), ('2', 'FOB')], default='1', max_length=1)),
                ('valor_frete', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('volumes', models.CharField(blank=True, max_length=15, null=True)),
                ('peso_bruto', models.CharField(blank=True, max_length=15, null=True)),
                ('peso_liquido', models.CharField(blank=True, max_length=15, null=True)),
                ('marca', models.CharField(blank=True, max_length=15, null=True)),
                ('obs', models.TextField(blank=True, max_length=5000, null=True)),
                ('obs_nf', models.TextField(blank=True, max_length=5000, null=True)),
                ('valor_total_pedido', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('operacao', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='comercial.operacao')),
                ('pedido_origem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entregas', to='comercial.pedido')),
                ('transportadora', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='entregas_tranportadas', to='cadastro.parceiro')),
                ('vencimentos', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='entregas', to='comercial.vencimento')),
            ],
        ),
        migrations.CreateModel(
            name='Orcamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_orc', models.CharField(blank=True, max_length=15, null=True, verbose_name='Número Orçamento')),
                ('num_orc_cli', models.CharField(blank=True, max_length=15, null=True, verbose_name='Número Cliente')),
                ('data_cadastro', models.DateTimeField(auto_now_add=True, null=True)),
                ('data_previsao', models.DateTimeField(blank=True, null=True)),
                ('previsao_entrega', models.PositiveSmallIntegerField(blank=True, default=0, null=True, verbose_name='Previsão de entrega')),
                ('validade_orcamento', models.PositiveSmallIntegerField(blank=True, default=0, null=True, verbose_name='Validade do orçamento')),
                ('tipo_frete', models.CharField(choices=[('1', 'CIF'), ('2', 'FOB')], default='1', max_length=1)),
                ('valor_frete', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('obs', models.TextField(blank=True, max_length=5000, null=True)),
                ('valor_total_produtos', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('valor_total_orcamento', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('operacao', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='comercial.operacao')),
            ],
        ),
        migrations.CreateModel(
            name='Orcamento_origem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.CharField(blank=True, max_length=30, null=True, verbose_name='Nome')),
            ],
        ),
        migrations.CreateModel(
            name='Orcamento_status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.CharField(blank=True, max_length=30, null=True, verbose_name='Nome')),
            ],
        ),
        migrations.CreateModel(
            name='Orcamento_item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qtd', models.DecimalField(decimal_places=3, default=0, max_digits=15, verbose_name='Qtd')),
                ('pr_unit', models.DecimalField(decimal_places=3, default=0, max_digits=15, verbose_name='Preço Unit.')),
                ('aliq_ICMS', models.DecimalField(decimal_places=3, default=0, max_digits=15, verbose_name='Aliq ICMS')),
                ('aliq_IPI', models.DecimalField(decimal_places=3, default=0, max_digits=15, verbose_name='Aliq IPI')),
                ('val_ICMS', models.DecimalField(decimal_places=3, default=0, max_digits=15, verbose_name='Valor ICMS')),
                ('val_IPI', models.DecimalField(decimal_places=3, default=0, max_digits=15, verbose_name='Valor IPI')),
                ('obs', models.CharField(blank=True, max_length=500, null=True)),
                ('orcamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comercial.orcamento')),
                ('produto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='prod.prod')),
            ],
        ),
        migrations.AddField(
            model_name='orcamento',
            name='origem',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='comercial.orcamento_origem'),
        ),
        migrations.AddField(
            model_name='orcamento',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='comercial.orcamento_status'),
        ),
        migrations.AddField(
            model_name='orcamento',
            name='transportadora',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='orcamentos', to='cadastro.parceiro'),
        ),
        migrations.AddField(
            model_name='orcamento',
            name='vencimentos',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='orcamentos', to='comercial.vencimento'),
        ),
        migrations.CreateModel(
            name='Entrega_item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qtd', models.DecimalField(decimal_places=3, default=0, max_digits=15, verbose_name='Qtd')),
                ('pr_unit', models.DecimalField(decimal_places=3, default=0, max_digits=15, verbose_name='Preço Unit.')),
                ('aliq_ICMS', models.DecimalField(decimal_places=3, default=0, max_digits=15, verbose_name='Aliq ICMS')),
                ('aliq_IPI', models.DecimalField(decimal_places=3, default=0, max_digits=15, verbose_name='Aliq IPI')),
                ('val_ICMS', models.DecimalField(decimal_places=3, default=0, max_digits=15, verbose_name='Valor ICMS')),
                ('val_IPI', models.DecimalField(decimal_places=3, default=0, max_digits=15, verbose_name='Valor IPI')),
                ('codigo_cfop', models.CharField(max_length=4, verbose_name='CFOP')),
                ('obs', models.CharField(blank=True, max_length=50, null=True)),
                ('inf_adic', models.CharField(blank=True, max_length=500, null=True)),
                ('entrega', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comercial.entrega')),
                ('pedido_item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='comercial.pedido_item')),
                ('produto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='prod.prod')),
            ],
        ),
    ]