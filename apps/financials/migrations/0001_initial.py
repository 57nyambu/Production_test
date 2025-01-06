# Generated by Django 5.1.3 on 2025-01-06 18:42

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
            name='AdminMarketingExp',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('exp_type', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('value', models.DecimalField(decimal_places=2, max_digits=15)),
                ('type', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Capex',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('maintenance_capex', models.DecimalField(decimal_places=2, max_digits=5)),
                ('growth_capex', models.DecimalField(decimal_places=2, max_digits=5)),
                ('asset_lifespan', models.PositiveIntegerField()),
                ('capitalized_costs', models.DecimalField(decimal_places=2, max_digits=15)),
                ('assets', models.ManyToManyField(to='financials.asset')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CompanyInformation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company_name', models.CharField(max_length=255)),
                ('industry', models.CharField(max_length=255)),
                ('company_stage', models.CharField(max_length=25)),
                ('funding_type', models.CharField(max_length=25)),
                ('fiscal_year_end', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CostStracture',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('raw_material', models.DecimalField(decimal_places=2, max_digits=15)),
                ('direct_labor', models.DecimalField(decimal_places=2, max_digits=15)),
                ('man_overhead', models.DecimalField(decimal_places=2, max_digits=15)),
                ('total_cogs', models.DecimalField(decimal_places=2, max_digits=15)),
                ('fixed_cost', models.DecimalField(decimal_places=2, max_digits=15)),
                ('variable_cost', models.DecimalField(decimal_places=2, max_digits=15)),
                ('cd_raw_material', models.DecimalField(decimal_places=2, max_digits=15)),
                ('cd_direct_labor', models.DecimalField(decimal_places=2, max_digits=15)),
                ('cd_man_overhead', models.DecimalField(decimal_places=2, max_digits=15)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DividendPolicy',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('payout_ratio', models.DecimalField(decimal_places=2, max_digits=4)),
                ('div_per_share', models.DecimalField(decimal_places=2, max_digits=4)),
                ('div_growth_rt', models.DecimalField(decimal_places=2, max_digits=4)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EmployeeInfo',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('position', models.CharField(max_length=255)),
                ('salary', models.DecimalField(decimal_places=2, max_digits=10)),
                ('count', models.PositiveIntegerField()),
                ('salary_growth_rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AllExpenses',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('average_selling_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('units_sold', models.PositiveIntegerField()),
                ('admin_marketing_exp', models.ManyToManyField(to='financials.adminmarketingexp')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('employee_info', models.ManyToManyField(to='financials.employeeinfo')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HistoricalFinData',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('revenue', models.DecimalField(decimal_places=2, max_digits=15)),
                ('cogs', models.DecimalField(decimal_places=2, max_digits=15)),
                ('salaries', models.DecimalField(decimal_places=2, max_digits=15)),
                ('rent', models.DecimalField(decimal_places=2, max_digits=15)),
                ('marketing', models.DecimalField(decimal_places=2, max_digits=15)),
                ('technology', models.DecimalField(decimal_places=2, max_digits=15)),
                ('insurance', models.DecimalField(decimal_places=2, max_digits=15)),
                ('other', models.DecimalField(decimal_places=2, max_digits=15)),
                ('total_operating_expenses', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('cash_equivs', models.DecimalField(decimal_places=2, max_digits=15)),
                ('acc_receivable', models.DecimalField(decimal_places=2, max_digits=15)),
                ('inventory', models.DecimalField(decimal_places=2, max_digits=15)),
                ('fixed_assets', models.DecimalField(decimal_places=2, max_digits=15)),
                ('acc_payable', models.DecimalField(decimal_places=2, max_digits=15)),
                ('short_debt', models.DecimalField(decimal_places=2, max_digits=15)),
                ('long_debt', models.DecimalField(decimal_places=2, max_digits=15)),
                ('paid_in_cap', models.DecimalField(decimal_places=2, max_digits=15)),
                ('retained_earning', models.DecimalField(decimal_places=2, max_digits=15)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='IndustryMetrics',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('market_share', models.DecimalField(decimal_places=2, max_digits=5)),
                ('industry_growth_rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('competitor_count', models.PositiveIntegerField()),
                ('market_size', models.DecimalField(decimal_places=2, max_digits=15)),
                ('corporate_tax_rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('inflation_rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('gdp_growth_rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('interest_rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RevenueStream',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=50)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RevenueDrivers',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('average_selling_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('units_sold', models.PositiveIntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('revenue_streams', models.ManyToManyField(to='financials.revenuestream')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WorkingCapital',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('days_receivables', models.PositiveIntegerField()),
                ('days_inventory', models.PositiveIntegerField()),
                ('days_payables', models.PositiveIntegerField()),
                ('working_capital_days', models.PositiveIntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
