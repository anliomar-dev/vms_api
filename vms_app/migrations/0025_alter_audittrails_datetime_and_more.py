# Generated by Django 5.1.5 on 2025-01-30 13:38

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vms_app', '0024_alter_audittrails_datetime_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audittrails',
            name='datetime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='redemption',
            name='redemption_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='voucher',
            name='date_time_created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='voucherrequest',
            name='date_time_recorded',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]
