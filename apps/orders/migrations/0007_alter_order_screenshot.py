# Generated by Django 4.2.5 on 2023-09-19 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_rename_ordermodel_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='screenshot',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
