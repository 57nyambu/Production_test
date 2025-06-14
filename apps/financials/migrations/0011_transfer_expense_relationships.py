# Generated by Django 5.1.3 on 2025-06-11 18:52

from django.db import migrations

def transfer_relationships(apps, schema_editor):
    AllExpenses = apps.get_model('financials', 'AllExpenses')
    
    # Process all AllExpenses instances
    for expenses in AllExpenses.objects.all():
        # Transfer EmployeeInfo relationships
        employees = expenses.employee_info.all()
        for employee in employees:
            employee.all_expenses = expenses
            employee.save()
            
        # Transfer AdminMarketingExp relationships
        admin_exps = expenses.admin_marketing_exp.all()
        for admin_exp in admin_exps:
            admin_exp.all_expenses = expenses
            admin_exp.save()

def reverse_relationships(apps, schema_editor):
    EmployeeInfo = apps.get_model('financials', 'EmployeeInfo')
    AdminMarketingExp = apps.get_model('financials', 'AdminMarketingExp')
    
    for employee in EmployeeInfo.objects.all():
        if employee.all_expenses:
            employee.all_expenses.employee_info.add(employee)
            employee.all_expenses = None
            employee.save()
    
    for admin_exp in AdminMarketingExp.objects.all():
        if admin_exp.all_expenses:
            admin_exp.all_expenses.admin_marketing_exp.add(admin_exp)
            admin_exp.all_expenses = None
            admin_exp.save()

class Migration(migrations.Migration):
    dependencies = [
        ('financials', '0010_adminmarketingexp_all_expenses_and_more'),
    ]

    operations = [
        migrations.RunPython(transfer_relationships, reverse_relationships),
    ]