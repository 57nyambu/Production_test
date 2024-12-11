from django.db import models
from .company import CompanyInformation

class Employee(models.Model):
    company = models.ForeignKey(CompanyInformation, on_delete=models.CASCADE)
    position = models.CharField(max_length=255)
    salary = models.DecimalField(max_digits=15, decimal_places=2)

class EmployeeMetrics(models.Model):
    company = models.OneToOneField(CompanyInformation, on_delete=models.CASCADE)
    total_employee_count = models.PositiveIntegerField()
    average_salary = models.DecimalField(max_digits=15, decimal_places=2)
    salary_growth = models.DecimalField(max_digits=5, decimal_places=2)  # As percentage
