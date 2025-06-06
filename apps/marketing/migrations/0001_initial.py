# Generated by Django 5.1.3 on 2025-03-03 14:03

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
            name='MarketingMetrics',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('fiscal_year', models.IntegerField(unique=True)),
                ('yearly_marketing_cost', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('number_of_months_in_year', models.IntegerField(default=12)),
                ('monthly_marketing_cost', models.DecimalField(decimal_places=2, editable=False, max_digits=15)),
                ('cac', models.DecimalField(decimal_places=2, max_digits=15)),
                ('number_of_customers', models.IntegerField(editable=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MarketingComponent',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(max_length=255)),
                ('cost', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to=settings.AUTH_USER_MODEL)),
                ('marketing_metrics', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='marketing_components', to='marketing.marketingmetrics')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
