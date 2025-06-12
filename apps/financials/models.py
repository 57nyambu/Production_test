from django.db import models
import uuid
from apps.accounts.models import CustomUser
from decimal import Decimal

# Base Model with UUID
class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="%(class)ss")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CompanyInformation(BaseModel):
    company_name = models.CharField(max_length=255)
    industry = models.CharField(max_length=255)
    company_stage = models.CharField(max_length=25)
    funding_type = models.CharField(max_length=25)
    fiscal_year_end = models.DateField()


# Working Capital
class WorkingCapital(BaseModel):
    days_receivables = models.PositiveIntegerField()
    days_inventory = models.PositiveIntegerField()
    days_payables = models.PositiveIntegerField()
    working_capital_days = models.PositiveIntegerField()
    

class RevenueDrivers(BaseModel):
    percentage_comm = models.DecimalField(max_digits=5, decimal_places=2) 
    units_sold = models.PositiveIntegerField()
    # Quartely seasonality
    q1 = models.DecimalField(default=25, max_digits=5, decimal_places=2)
    q2 = models.DecimalField(default=25, max_digits=5, decimal_places=2)
    q3 = models.DecimalField(default=25, max_digits=5, decimal_places=2)
    q4 = models.DecimalField(default=25, max_digits=5, decimal_places=2)

    def calculate_revenue(self):
        total_revenue = Decimal('0.00')
        for stream in self.revenue_streams.all():
            # Apply commission as a percentage to the revenue from units sold
            commission_amount = (self.percentage_comm / Decimal('100.0')) * self.units_sold
            stream_revenue = stream.amount or Decimal('0.00')
            total_revenue += stream_revenue + commission_amount
        return total_revenue

    def __str__(self):
        return f"Revenue Drivers (Commission: {self.percentage_comm}%, Total Revenue: {self.calculate_revenue()})"


class RevenueStream(BaseModel):
    driver = models.ForeignKey(RevenueDrivers, on_delete=models.CASCADE, related_name='revenue_streams')
    name = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.type})"


# Revenue & Expenses
class CostStracture(BaseModel):
    # cogs (direct cost)
    raw_material = models.DecimalField(max_digits=15, decimal_places=2)
    direct_labor = models.DecimalField(max_digits=15, decimal_places=2)
    man_overhead = models.DecimalField(max_digits=15, decimal_places=2)
    total_cogs = models.DecimalField(max_digits=15, decimal_places=2)
    
    fixed_cost = models.DecimalField(max_digits=15, decimal_places=2)
    variable_cost = models.DecimalField(max_digits=15, decimal_places=2)

    cd_raw_material = models.DecimalField(max_digits=15, decimal_places=2)
    cd_direct_labor = models.DecimalField(max_digits=15, decimal_places=2)
    cd_man_overhead = models.DecimalField(max_digits=15, decimal_places=2)

    def cogs_calculation(self):
        return (
            self.raw_material + self.direct_labor + self.man_overhead +
            self.fixed_cost + self.variable_cost + self.cd_raw_material +
            self.cd_direct_labor + self.cd_man_overhead
        )


class EmployeeInfo(BaseModel):
    all_expenses = models.ForeignKey('AllExpenses', on_delete=models.CASCADE, related_name='employees', null=True, blank=True)
    position = models.CharField(max_length=255)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    count = models.PositiveIntegerField()
    salary_growth_rate = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.position} (Count: {self.count}, Salary Growth Rate: {self.salary_growth_rate}%)"

class AdminMarketingExp(BaseModel):
    all_expenses = models.ForeignKey('AllExpenses', on_delete=models.CASCADE, related_name='admin_expenses', null=True, blank=True)
    exp_type = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return f"{self.exp_type} (Amount: {self.amount})"

class AllExpenses(BaseModel):
    employee_info = models.ManyToManyField(EmployeeInfo)
    salary_growth_rate = models.DecimalField(max_digits=5, decimal_places=2)
    admin_marketing_exp = models.ManyToManyField(AdminMarketingExp)

    def __str__(self):
        return f"All Expenses (ASP: {self.average_selling_price}, Units Sold: {self.units_sold})"
    
    def all_expens_calc(self):
        employee_cost = sum(emp.salary * emp.count for emp in self.employee_info.all())
        admin_cost = sum(admin.amount for admin in self.admin_marketing_exp.all())

        return (employee_cost + admin_cost)


# Capital expenditure planning
class Asset(BaseModel):
    name = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=15, decimal_places=2)
    type = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.type}) - Value: {self.value}"

class Capex(BaseModel):
    maintenance_capex = models.DecimalField(max_digits=5, decimal_places=2)
    growth_capex = models.DecimalField(max_digits=5, decimal_places=2)
    asset_lifespan = models.PositiveIntegerField()
    capitalized_costs = models.DecimalField(max_digits=15, decimal_places=2)
    assets = models.ManyToManyField(Asset)

    def __str__(self):
        return f"Capex (Maintenance: {self.maintenance_capex}, Growth: {self.growth_capex})"



# Dividend policy
class DividendPolicy(BaseModel):
    payout_ratio = models.DecimalField(max_digits=4, decimal_places=2)
    div_per_share = models.DecimalField(max_digits=4, decimal_places=2)
    div_growth_rt = models.DecimalField(max_digits=4, decimal_places=2)


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


# Historical financial details
class HistoricalFinData(BaseModel):
    # Income Statement
    revenue = models.DecimalField(max_digits=15, decimal_places=2)
    cogs = models.DecimalField(max_digits=15, decimal_places=2)

    #operating expenses
    salaries = models.DecimalField(max_digits=15, decimal_places=2)
    rent = models.DecimalField(max_digits=15, decimal_places=2)
    marketing = models.DecimalField(max_digits=15, decimal_places=2)
    technology = models.DecimalField(max_digits=15, decimal_places=2)
    insurance = models.DecimalField(max_digits=15, decimal_places=2)
    other = models.DecimalField(max_digits=15, decimal_places=2)
    total_operating_expenses = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    #Balance sheet
    cash_equivs = models.DecimalField(max_digits=15, decimal_places=2)
    acc_receivable = models.DecimalField(max_digits=15, decimal_places=2)
    inventory = models.DecimalField(max_digits=15, decimal_places=2)
    fixed_assets = models.DecimalField(max_digits=15, decimal_places=2)

    #Liabilities
    acc_payable = models.DecimalField(max_digits=15, decimal_places=2)
    short_debt = models.DecimalField(max_digits=15, decimal_places=2)
    long_debt = models.DecimalField(max_digits=15, decimal_places=2)

    # Equity
    paid_in_cap = models.DecimalField(max_digits=15, decimal_places=2)
    retained_earning = models.DecimalField(max_digits=15, decimal_places=2)
