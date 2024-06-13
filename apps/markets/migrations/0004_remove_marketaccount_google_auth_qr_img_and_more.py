# Generated by Django 5.0.4 on 2024-05-27 22:19

import django_cryptography.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('markets', '0003_marketaccount_google_auth_qr_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='marketaccount',
            name='google_auth_qr_img',
        ),
        migrations.AddField(
            model_name='marketaccount',
            name='google_auth_totp_code',
            field=django_cryptography.fields.encrypt(models.CharField(blank=True, default=None, max_length=20, null=True)),
        ),
    ]