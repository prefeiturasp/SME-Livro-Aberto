# Generated by Django 2.2.7 on 2019-12-03 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regionalizacao', '0039_auto_20191203_1329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grupo',
            name='name',
            field=models.CharField(max_length=150, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='subgrupo',
            unique_together={('grupo', 'name')},
        ),
    ]
