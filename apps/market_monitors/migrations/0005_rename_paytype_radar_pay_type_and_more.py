# Generated by Django 5.0.4 on 2024-05-14 23:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('market_monitors', '0004_alter_radar_tradetype'),
    ]

    operations = [
        migrations.RenameField(
            model_name='radar',
            old_name='payType',
            new_name='pay_type',
        ),
        migrations.RenameField(
            model_name='radar',
            old_name='tradeType',
            new_name='trade_type',
        ),
    ]