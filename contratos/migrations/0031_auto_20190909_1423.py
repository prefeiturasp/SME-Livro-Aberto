# Generated by Django 2.2.3 on 2019-09-09 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contratos', '0030_auto_20190909_1350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoriacontratofromto',
            name='categoria_desc',
            field=models.TextField(verbose_name='Descrição da categoria'),
        ),
        migrations.AlterField(
            model_name='categoriacontratofromto',
            name='categoria_name',
            field=models.CharField(max_length=60, verbose_name='Nome da categoria'),
        ),
    ]
