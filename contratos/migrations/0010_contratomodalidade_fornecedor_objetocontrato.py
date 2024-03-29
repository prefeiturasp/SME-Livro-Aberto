# Generated by Django 2.2.3 on 2019-08-03 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contratos', '0009_contratocategoria'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContratoModalidade',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('desc', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Fornecedor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('razao_social', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='ObjetoContrato',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.TextField()),
            ],
        ),
    ]
