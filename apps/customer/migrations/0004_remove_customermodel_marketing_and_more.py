# Generated by Django 5.1.3 on 2025-03-26 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_customermodel_marketing'),
        ('marketing', '0006_alter_marketingmetrics_cac_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customermodel',
            name='marketing',
        ),
        migrations.AddField(
            model_name='customermodel',
            name='growth_rate',
            field=models.ManyToManyField(to='marketing.growthrate'),
        ),
    ]
