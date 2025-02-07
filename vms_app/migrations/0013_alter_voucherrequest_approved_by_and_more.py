# Generated by Django 5.1.5 on 2025-01-23 07:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vms_app', '0012_alter_voucherrequest_recorded_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voucherrequest',
            name='approved_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='approved_requests', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='voucherrequest',
            name='date_time_approved',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
