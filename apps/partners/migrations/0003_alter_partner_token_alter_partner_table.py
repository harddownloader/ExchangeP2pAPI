# Generated by Django 4.2.5 on 2023-09-19 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0002_alter_partner_google_doc_id_alter_partner_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partner',
            name='token',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterModelTable(
            name='partner',
            table='auth_partner',
        ),
    ]
