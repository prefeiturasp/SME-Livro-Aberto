# Generated by Django 2.1.5 on 2019-01-24 16:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('budget_execution', '0013_execucao_is_minimo_legal'),
    ]

    operations = [
        migrations.AddField(
            model_name='minimolegal',
            name='execucao',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='budget_execution.Execucao'),
        ),
    ]
