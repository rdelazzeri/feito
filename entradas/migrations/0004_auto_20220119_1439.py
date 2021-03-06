# Generated by Django 3.2.7 on 2022-01-19 17:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comercial', '0031_auto_20220117_1149'),
        ('entradas', '0003_auto_20220119_1136'),
    ]

    operations = [
        migrations.AddField(
            model_name='nf_entrada',
            name='base_calc_icms',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=13),
        ),
        migrations.AddField(
            model_name='nf_entrada',
            name='base_calc_icms_subst',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=13),
        ),
        migrations.AddField(
            model_name='nf_entrada',
            name='desconto',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=13),
        ),
        migrations.AddField(
            model_name='nf_entrada',
            name='valor_icms',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=13),
        ),
        migrations.AddField(
            model_name='nf_entrada',
            name='valor_icms_subst',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=13),
        ),
        migrations.AddField(
            model_name='nf_entrada',
            name='valor_ipi',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=13),
        ),
        migrations.AddField(
            model_name='nf_entrada',
            name='valor_seguro',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=13),
        ),
        migrations.AlterField(
            model_name='nf_entrada',
            name='valor_frete',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=13),
        ),
        migrations.AlterField(
            model_name='nf_entrada',
            name='valor_outras_desp',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=13),
        ),
        migrations.AlterField(
            model_name='nf_entrada',
            name='valor_total_nota',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=13),
        ),
        migrations.AlterField(
            model_name='nf_entrada',
            name='valor_total_produtos',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=13),
        ),
        migrations.AlterField(
            model_name='nf_entrada',
            name='vencimento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='comercial.vencimento'),
        ),
        migrations.AlterField(
            model_name='nf_entrada_itens',
            name='aliq_icms',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='nf_entrada_itens',
            name='aliq_ipi',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='nf_entrada_itens',
            name='preco_tot',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=13),
        ),
        migrations.AlterField(
            model_name='nf_entrada_itens',
            name='preco_unit',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=13),
        ),
        migrations.AlterField(
            model_name='nf_entrada_itens',
            name='qtd',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=13),
        ),
        migrations.AlterField(
            model_name='nf_entrada_itens',
            name='valor_ipi',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=13),
        ),
        migrations.AlterField(
            model_name='ordem_compra',
            name='valor_frete',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=13),
        ),
        migrations.AlterField(
            model_name='ordem_compra',
            name='valor_outras_desp',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=13),
        ),
        migrations.AlterField(
            model_name='ordem_compra',
            name='valor_total_nota',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=13),
        ),
        migrations.AlterField(
            model_name='ordem_compra',
            name='valor_total_produtos',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=13),
        ),
        migrations.AlterField(
            model_name='ordem_compra_itens',
            name='aliq_icms',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='ordem_compra_itens',
            name='aliq_ipi',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='ordem_compra_itens',
            name='preco_tot',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=13),
        ),
        migrations.AlterField(
            model_name='ordem_compra_itens',
            name='preco_unit',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=13),
        ),
        migrations.AlterField(
            model_name='ordem_compra_itens',
            name='qtd',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=13),
        ),
        migrations.AlterField(
            model_name='ordem_compra_itens',
            name='valor_ipi',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=13),
        ),
        migrations.AlterField(
            model_name='solicitacao_material',
            name='valor_total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=13),
        ),
        migrations.AlterField(
            model_name='solicitacao_material_item',
            name='aliq_icms',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='solicitacao_material_item',
            name='aliq_ipi',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='solicitacao_material_item',
            name='preco_unit',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=13),
        ),
        migrations.AlterField(
            model_name='solicitacao_material_item',
            name='qtd',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=13),
        ),
        migrations.AlterField(
            model_name='solicitacao_material_item',
            name='valor_ipi',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=13),
        ),
        migrations.AlterField(
            model_name='solicitacao_material_item',
            name='valor_tot',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=13),
        ),
        migrations.AlterField(
            model_name='solicitacao_material_item',
            name='valor_tot_ipi',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=13),
        ),
    ]
