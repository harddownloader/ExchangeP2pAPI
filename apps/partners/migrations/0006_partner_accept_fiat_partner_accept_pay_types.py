# Generated by Django 5.0.4 on 2024-05-08 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('markets', '0001_initial'),
        ('partners', '0005_alter_partner_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='partner',
            name='accept_fiat',
            field=models.ManyToManyField(blank=True, to='markets.fiatcurrency'),
        ),
        migrations.AddField(
            model_name='partner',
            name='accept_pay_types',
            field=models.ManyToManyField(blank=True, to='markets.paytypes'),
        ),
    ]
