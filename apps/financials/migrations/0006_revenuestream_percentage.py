# Generated by Django 5.1.3 on 2025-05-16 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financials', '0005_revenuedrivers_q1_revenuedrivers_q2_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='revenuestream',
            name='percentage',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, null=True),
        ),
    ]
