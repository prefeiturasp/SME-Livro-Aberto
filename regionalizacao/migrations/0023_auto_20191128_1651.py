# Generated by Django 2.2.7 on 2019-11-28 16:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('regionalizacao', '0022_auto_20191128_1650'),
    ]

    operations = [
        migrations.RenameField(
            model_name='distrito',
            old_name='code',
            new_name='coddist',
        ),
    ]
