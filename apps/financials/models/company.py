from django.db import models

class CompanyInformation(models.Model):
    STAGES = [('startup', 'Startup'), ('growth', 'Growth'), ('mature', 'Mature')]
    FUNDING_TYPES = [
        ('bootstrapped', 'Bootstrapped'),
        ('seed', 'Seed'),
        ('seriesA', 'Series A'),
        ('seriesB', 'Series B'),
        ('seriesC', 'Series C'),
        ('public', 'Public'),
        ('private', 'Private'),
    ]

    company_name = models.CharField(max_length=255)
    industry = models.CharField(max_length=255)
    company_stage = models.CharField(choices=STAGES, max_length=50)
    funding_type = models.CharField(choices=FUNDING_TYPES, max_length=50)
    fiscal_year_end = models.DateField()

    def __str__(self):
        return self.company_name
