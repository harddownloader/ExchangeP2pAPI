# Generated by Django 5.0.4 on 2024-05-13 16:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('markets', '0002_alter_marketaccount_api_key_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Radar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Binance, Bybit, WhiteBit,...', max_length=128)),
                ('description', models.TextField(help_text='Description')),
                ('doc_id', models.CharField(help_text='google spreadsheet doc id', max_length=50)),
                ('sheet_name', models.CharField(help_text='google spreadsheet table name', max_length=50)),
                ('first_row', models.IntegerField(default=2, help_text='1, 2, 3,...')),
                ('fiat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='markets.fiatcurrency')),
                ('payType', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='markets.paytypes')),
            ],
            options={
                'db_table_comment': 'reports system about p2p orders on the market',
            },
        ),
    ]