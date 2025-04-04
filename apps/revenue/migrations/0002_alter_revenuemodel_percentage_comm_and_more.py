# Generated by Django 5.1.3 on 2025-03-27 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('revenue', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='revenuemodel',
            name='percentage_comm',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='revenuemodel',
            name='units_sold',
            field=models.PositiveIntegerField(verbose_name=0),
        ),
    ]
