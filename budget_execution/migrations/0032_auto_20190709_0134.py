# Generated by Django 2.2.2 on 2019-07-09 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget_execution', '0031_auto_20190704_0059'),
    ]

    operations = [
        migrations.AddField(
            model_name='execucao',
            name='vl_pago',
            field=models.DecimalField(decimal_places=2, max_digits=17, null=True),
        ),
        migrations.AddField(
            model_name='execucaotemp',
            name='vl_pago',
            field=models.DecimalField(decimal_places=2, max_digits=17, null=True),
        ),
    ]
