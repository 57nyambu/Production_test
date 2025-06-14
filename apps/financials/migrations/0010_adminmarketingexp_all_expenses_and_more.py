# Generated by Django 5.1.3 on 2025-06-11 18:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financials', '0009_alter_revenuestream_amount_alter_revenuestream_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminmarketingexp',
            name='all_expenses',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='admin_expenses', to='financials.allexpenses'),
        ),
        migrations.AddField(
            model_name='employeeinfo',
            name='all_expenses',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='financials.allexpenses'),
        ),
    ]
