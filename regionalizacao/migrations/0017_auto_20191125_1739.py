# Generated by Django 2.2.7 on 2019-11-25 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regionalizacao', '0016_escola'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tipoescola',
            name='code',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]
