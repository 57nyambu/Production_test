from django.db import models
import uuid

# Base Model with UUID
class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# Revenue & Expenses
class RevenueExpenses(BaseModel):
    revenue = models.DecimalField(max_digits=15, decimal_places=2)
    expenses = models.DecimalField(max_digits=15, decimal_places=2)
    cost_of_goods_sold = models.DecimalField(max_digits=15, decimal_places=2)
    direct_labor = models.DecimalField(max_digits=15, decimal_places=2)
    manufacturing_overhead = models.DecimalField(max_digits=15, decimal_places=2)
    gross_profit = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    # Operating Expenses
    salaries = models.DecimalField(max_digits=15, decimal_places=2)
    rent = models.DecimalField(max_digits=15, decimal_places=2)
    marketing = models.DecimalField(max_digits=15, decimal_places=2)
    technology = models.DecimalField(max_digits=15, decimal_places=2)
    insurance = models.DecimalField(max_digits=15, decimal_places=2)
    other = models.DecimalField(max_digits=15, decimal_places=2)
    total_operating_expenses = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

# Working Capital
class WorkingCapital(BaseModel):
    days_receivables = models.PositiveIntegerField()
    days_inventory = models.PositiveIntegerField()
    days_payables = models.PositiveIntegerField()
    working_capital_days = models.PositiveIntegerField()

# Industry Metrics
class IndustryMetrics(BaseModel):
    # Micro Economics
    market_share = models.DecimalField(max_digits=5, decimal_places=2)
    industry_growth_rate = models.DecimalField(max_digits=5, decimal_places=2)
    competitor_count = models.PositiveIntegerField()
    market_size = models.DecimalField(max_digits=15, decimal_places=2)

    # Macro Economics
    corporate_tax_rate = models.DecimalField(max_digits=5, decimal_places=2)
    inflation_rate = models.DecimalField(max_digits=5, decimal_places=2)
    gdp_growth_rate = models.DecimalField(max_digits=5, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)

# Employee & Salary Information (SG&A)
class EmployeeSalaryInfo(BaseModel):
    salary_growth = models.DecimalField(max_digits=5, decimal_places=2)

class Staff(BaseModel):
    employee_salary_info = models.ForeignKey(EmployeeSalaryInfo, related_name='staff', on_delete=models.CASCADE)
    position = models.CharField(max_length=255)
    salary = models.DecimalField(max_digits=15, decimal_places=2)
    count = models.PositiveIntegerField()

class AdminExpense(BaseModel):
    employee_salary_info = models.ForeignKey(EmployeeSalaryInfo, related_name='admin_expenses', on_delete=models.CASCADE)
    type = models.CharField(
        max_length=50,
        choices=[
            ('Rent', 'Rent'),
            ('Marketing', 'Marketing'),
            ('Subscription', 'Subscription'),
            ('Accounting', 'Accounting'),
            ('Legal', 'Legal'),
            ('Utility', 'Utility'),
            ('Other', 'Other'),
        ],
    )
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.TextField(null=True, blank=True)

# Capital Expenditure
class CapitalExpenditure(BaseModel):
    maintenance_capex = models.DecimalField(max_digits=5, decimal_places=2)
    growth_capex = models.DecimalField(max_digits=5, decimal_places=2)
    asset_lifespan = models.PositiveIntegerField()
    capitalized_costs = models.DecimalField(max_digits=15, decimal_places=2)

class CapitalAsset(BaseModel):
    capital_expenditure = models.ForeignKey(CapitalExpenditure, related_name='capital_assets', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=15, decimal_places=2)
    type = models.CharField(
        max_length=50,
        choices=[
            ('Land', 'Land'),
            ('Buildings', 'Buildings'),
            ('Machinery', 'Machinery'),
            ('Vehicles', 'Vehicles'),
            ('Equipment', 'Equipment'),
            ('Furniture', 'Furniture'),
            ('Technology', 'Technology'),
            ('Other', 'Other'),
        ],
    )
    description = models.TextField(null=True, blank=True)
