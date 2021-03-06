# Generated by Django 3.2.7 on 2021-11-25 17:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('prod', '0010_alter_prod_cod'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.CharField(max_length=15, verbose_name='Número')),
                ('data_cadastro', models.DateTimeField(auto_now_add=True, null=True)),
                ('data_previsao', models.DateTimeField(blank=True, null=True)),
                ('tipo_frete', models.CharField(blank=True, choices=[('1', 'CIF'), ('2', 'FOB')], max_length=1)),
                ('obs', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vencimento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vencimentos', models.CharField(max_length=30, verbose_name='Vencimentos')),
            ],
        ),
        migrations.CreateModel(
            name='Pedido_item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qtd', models.DecimalField(decimal_places=3, default=0, max_digits=15, verbose_name='Qtd')),
                ('pr_unit', models.DecimalField(decimal_places=3, default=0, max_digits=15, verbose_name='Preço Unit.')),
                ('pr_tot', models.DecimalField(decimal_places=3, default=0, max_digits=15, verbose_name='Preço Total.')),
                ('aliq_ICMS', models.DecimalField(decimal_places=3, default=0, max_digits=15, verbose_name='Aliq ICMS')),
                ('aliq_IPI', models.DecimalField(decimal_places=3, default=0, max_digits=15, verbose_name='Aliq IPI')),
                ('val_ICMS', models.DecimalField(decimal_places=3, default=0, max_digits=15, verbose_name='Valor ICMS')),
                ('val_IPI', models.DecimalField(decimal_places=3, default=0, max_digits=15, verbose_name='Valor IPI')),
                ('obs', models.CharField(blank=True, max_length=50, null=True)),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='prod.prod')),
            ],
        ),
    ]
