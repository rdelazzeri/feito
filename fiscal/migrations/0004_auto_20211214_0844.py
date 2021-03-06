# Generated by Django 3.2.7 on 2021-12-14 11:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fiscal', '0003_nf_config_aliq_credito_simples'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pre_nota_entrega',
            name='pre_nota_transporte',
        ),
        migrations.AddField(
            model_name='pre_nota_entrega',
            name='pre_nota',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='entrega', to='fiscal.pre_nota'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pre_nota_fatura',
            name='pre_nota',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='fatura', to='fiscal.pre_nota'),
        ),
        migrations.AlterField(
            model_name='pre_nota_parcelas',
            name='pre_nota',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parcelas', to='fiscal.pre_nota'),
        ),
        migrations.AlterField(
            model_name='pre_nota_pedido',
            name='pre_nota',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='pedido', to='fiscal.pre_nota'),
        ),
        migrations.AlterField(
            model_name='pre_nota_transporte',
            name='pre_nota',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='transporte', to='fiscal.pre_nota'),
        ),
    ]
