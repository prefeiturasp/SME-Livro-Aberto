# Generated by Django 2.2.7 on 2019-12-02 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regionalizacao', '0033_auto_20191202_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recurso',
            name='cost',
            field=models.FloatField(null=True),
        ),
    ]
