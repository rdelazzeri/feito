# Generated by Django 3.2.7 on 2021-12-21 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fiscal', '0008_alter_pre_nota_num_nf'),
    ]

    operations = [
        migrations.RenameField(
            model_name='nfe_transmissao',
            old_name='nfe_chave',
            new_name='chave',
        ),
        migrations.RenameField(
            model_name='nfe_transmissao',
            old_name='nfe_modelo',
            new_name='modelo',
        ),
        migrations.RenameField(
            model_name='nfe_transmissao',
            old_name='nfe_motivo',
            new_name='motivo',
        ),
        migrations.RenameField(
            model_name='nfe_transmissao',
            old_name='nfe_log',
            new_name='recibo',
        ),
        migrations.RenameField(
            model_name='nfe_transmissao',
            old_name='nfe_status',
            new_name='status',
        ),
        migrations.RenameField(
            model_name='nfe_transmissao',
            old_name='nfe_recibo',
            new_name='uuid',
        ),
        migrations.RemoveField(
            model_name='nfe_transmissao',
            name='nfe_danfe_link',
        ),
        migrations.RemoveField(
            model_name='nfe_transmissao',
            name='nfe_uuid',
        ),
        migrations.RemoveField(
            model_name='nfe_transmissao',
            name='nfe_xml_link',
        ),
        migrations.AddField(
            model_name='nfe_transmissao',
            name='danfe',
            field=models.URLField(blank=True, max_length=3000, null=True),
        ),
        migrations.AddField(
            model_name='nfe_transmissao',
            name='danfe_simples',
            field=models.URLField(blank=True, max_length=3000, null=True),
        ),
        migrations.AddField(
            model_name='nfe_transmissao',
            name='log',
            field=models.TextField(blank=True, max_length=3000, null=True),
        ),
        migrations.AddField(
            model_name='nfe_transmissao',
            name='xml',
            field=models.URLField(blank=True, max_length=3000, null=True),
        ),
    ]