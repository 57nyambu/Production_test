# Generated by Django 5.1.3 on 2025-02-11 08:32

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ret_rate', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('churn_rate', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('active_users', models.PositiveIntegerField(default=0)),
                ('nps_score', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('conversion_rate', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('lead_qual_score', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Customer',
                'verbose_name_plural': 'Customers',
            },
        ),
        migrations.CreateModel(
            name='MarketingType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Marketing',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('yearly_market_cost', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('cust_acq_cost', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('subscript_count', models.PositiveIntegerField(default=0)),
                ('subscript_dist', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('growth_rate', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to=settings.AUTH_USER_MODEL)),
                ('monthly_market_cost', models.ManyToManyField(to='combmodels.marketingtype')),
            ],
            options={
                'verbose_name': 'Marketing',
                'verbose_name_plural': 'Marketing',
            },
        ),
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('materials_cost', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('labor_cost', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('overhead_cost', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('sales_cost', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('marketing_cost', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('rd_cost', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('admin_cost', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('employee_count', models.PositiveIntegerField(default=0)),
                ('avg_salary', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('sal_growth_rate', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Operation',
                'verbose_name_plural': 'Operations',
            },
        ),
        migrations.CreateModel(
            name='Revenue',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('growth_rate', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('avg_sell_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('units_sold', models.PositiveIntegerField(default=0)),
                ('seas_factor', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Revenue',
                'verbose_name_plural': 'Revenues',
            },
        ),
    ]
