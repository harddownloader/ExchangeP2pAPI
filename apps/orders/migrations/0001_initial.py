# Generated by Django 4.2.5 on 2023-09-29 08:39

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('partners', '0005_alter_partner_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('orderId', models.CharField(max_length=255)),
                ('card', models.CharField(max_length=16)),
                ('payoutAmount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('callbackUrl', models.URLField()),
                ('callbackMethod', models.CharField(max_length=8)),
                ('callbackHeaders', models.TextField()),
                ('callbackBody', models.TextField()),
                ('status', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('rowNum', models.PositiveIntegerField(blank=True, default=None, null=True)),
                ('screenshot', models.CharField(blank=True, default='', max_length=255)),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='partners.partner')),
            ],
        ),
    ]
