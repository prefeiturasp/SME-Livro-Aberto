# Generated by Django 2.1.5 on 2019-02-11 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('from_to_handler', '0002_auto_20181219_1429'),
    ]

    operations = [
        migrations.CreateModel(
            name='DotacaoFromToSpreadsheet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spreadsheet', models.FileField(upload_to='from_to_handler/dotacao_spreadsheets', verbose_name='Planilha')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('data_extracted', models.BooleanField(default=False, editable=False)),
            ],
            options={
                'verbose_name': 'Planilha De-Para: Dotações Subgrupos Grupos',
                'verbose_name_plural': 'Planilhas De-Para: Dotações Subgrupos Grupos',
            },
        ),
    ]
