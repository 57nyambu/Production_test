# Generated by Django 5.1.3 on 2025-03-27 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0005_remove_customermodel_growth_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customermodel',
            name='customer_type',
            field=models.CharField(default='Organic', max_length=255),
        ),
    ]
