# Generated by Django 4.2.5 on 2023-09-25 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_alter_order_callbackbody_alter_order_callbackheaders_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='callbackUrl',
            field=models.URLField(),
        ),
    ]
