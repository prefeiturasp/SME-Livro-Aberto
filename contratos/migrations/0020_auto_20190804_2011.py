# Generated by Django 2.2.3 on 2019-08-04 20:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contratos', '0019_auto_20190804_2006'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ContratoCategoriaFromTo',
            new_name='CategoriaContratoFromTo',
        ),
        migrations.RenameModel(
            old_name='ContratoCategoriaFromToSpreadsheet',
            new_name='CategoriaContratoFromToSpreadsheet',
        ),
    ]
