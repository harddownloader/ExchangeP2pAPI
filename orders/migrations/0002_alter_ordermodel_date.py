# Generated by Django 4.2.5 on 2023-09-08 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordermodel',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
