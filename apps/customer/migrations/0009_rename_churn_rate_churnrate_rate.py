# Generated by Django 5.1.3 on 2025-04-15 12:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0008_remove_customermodel_growth_rate'),
    ]

    operations = [
        migrations.RenameField(
            model_name='churnrate',
            old_name='churn_rate',
            new_name='rate',
        ),
    ]
