from .models import CustomerModel, ChurnRate
from apps.marketing.models import GrowthRate, MarketingMetrics

from .models import CustomerModel, ChurnRate
from apps.marketing.models import GrowthRate

def get_organic_customer_metrics(user):
    customer_model = CustomerModel.objects.filter(user=user).first()
    if not customer_model:
        return None, "No customer data found."

    beginning_client = customer_model.beginning_client

    organic_distribution = customer_model.cust_type.filter(customer_type='online').first()
    if not organic_distribution:
        return None, "No online customer data found."
    organic_percentage = float(organic_distribution.percentage) / 100

    # Get all growth rates and churn rates, ensure year is int
    growth_rates = GrowthRate.objects.filter(user=user).order_by('year')
    churn_rates = ChurnRate.objects.filter(user=user).order_by('year')
    growth_rate_map = {int(g.year): float(g.rate) / 100 for g in growth_rates}
    churn_rate_map = {int(c.year): float(c.rate) / 100 for c in churn_rates}
    years = sorted(set(growth_rate_map.keys()) | set(churn_rate_map.keys()))

    # Get new clients per year from marketing model (assume yearly, else sum monthly)
    marketing_metrics = MarketingMetrics.objects.filter(user=user).order_by('id').first()
    new_clients_per_year = {}
    if marketing_metrics:
        for g in growth_rates:
            year = int(g.year)
            new_clients_per_year[year] = getattr(marketing_metrics, 'new_monthly_customers', 0) * 12

    current_beginning_client = int(beginning_client * organic_percentage)
    organic_metrics = []

    for year in years:
        churn_rate = churn_rate_map.get(year, 0)
        # Only assign the organic (online) share of new clients
        total_new_clients = int(new_clients_per_year.get(year, 0))
        new_clients = int(total_new_clients * organic_percentage)

        # Churn is applied to the sum of beginning and new clients
        total_clients_before_churn = current_beginning_client + new_clients
        churned_clients = int(total_clients_before_churn * churn_rate)
        closing_clients = total_clients_before_churn - churned_clients

        organic_metrics.append({
            "year": year,
            "beginning_client": current_beginning_client,
            "new_clients": new_clients,
            "churned_clients": churned_clients,
            "closing_clients": closing_clients,
        })

        current_beginning_client = closing_clients

    data = {
        "organic_metrics": organic_metrics
    }
    return data, None

def get_offline_customer_metrics(user):
    customer_model = CustomerModel.objects.filter(user=user).first()
    if not customer_model:
        return None, "No customer data found."

    beginning_client = customer_model.beginning_client

    # Get all customer type distributions as a dict: {type: percentage}
    distributions = {dist.customer_type: float(dist.percentage) / 100 for dist in customer_model.cust_type.all()}

    # Prepare growth and churn rates
    growth_rates = GrowthRate.objects.filter(user=user).order_by('year')
    churn_rates = ChurnRate.objects.filter(user=user).order_by('year')

    # Build year-to-rate maps (ensure year is int)
    growth_rate_map = {int(getattr(g, 'year', g.year)): float(g.rate) / 100 for g in growth_rates}
    churn_rate_map = {int(getattr(c, 'year', c.year)): float(c.rate) / 100 for c in churn_rates}
    years = sorted(set(growth_rate_map.keys()) | set(churn_rate_map.keys()))

    # Get new clients per year from marketing model
    marketing_metrics = MarketingMetrics.objects.filter(user=user).order_by('id').first()
    new_clients_per_year = {}
    if marketing_metrics:
        for g in growth_rates:
            year = int(g.year)
            new_clients_per_year[year] = getattr(marketing_metrics, 'new_monthly_customers', 0) * 12

    closing_clients_by_type = {ctype: [] for ctype in distributions.keys()}
    beginning_clients_by_type = {ctype: int(beginning_client * pct) for ctype, pct in distributions.items()}

    offline_metrics = []

    offline_percentage = distributions.get('offline', 0)

    for year in years:
        year_data = {}
        total_closing = 0
        total_new_clients = int(new_clients_per_year.get(year, 0))
        for ctype, pct in distributions.items():
            growth_rate = growth_rate_map.get(year, 0)
            churn_rate = churn_rate_map.get(year, 0)
            begin = beginning_clients_by_type[ctype]
            # Assign new clients from marketing according to type
            if total_new_clients > 0:
                new_clients = int(total_new_clients * pct)
            else:
                new_clients = int(begin * growth_rate)
            churned_clients = int(begin * churn_rate)
            closing = begin + new_clients - churned_clients
            year_data[ctype] = closing
            beginning_clients_by_type[ctype] = closing  # for next year
            total_closing += closing

            # For offline_metrics, only track offline type
            if ctype == "offline":
                offline_metrics.append({
                    "year": year,
                    "beginning_client": begin,
                    "new_clients": new_clients,
                    "churned_clients": churned_clients,
                    "closing_clients": closing,
                })

        for ctype, closing in year_data.items():
            percentage = (closing / total_closing * 100) if total_closing else 0
            closing_clients_by_type[ctype].append({
                "year": year,
                "customer_type": ctype,
                "closing_clients": closing,
                "percentage": round(percentage, 2)
            })

    # Flatten for serializer
    percentage_distributions = []
    for ctype, yearly_data in closing_clients_by_type.items():
        for entry in yearly_data:
            percentage_distributions.append({
                "year": entry["year"],
                "customer_type": entry["customer_type"],
                "percentage": entry["percentage"],
                "january_value": entry["closing_clients"]
            })

    data = {
        "offline_metrics": offline_metrics,
        "percentage_distributions": percentage_distributions,
    }
    return data, None

def get_combined_customer_metrics(user):
    organic_data, organic_error = get_organic_customer_metrics(user)
    offline_data, offline_error = get_offline_customer_metrics(user)
    if organic_error and offline_error:
        return None, f"{organic_error}; {offline_error}"
    return {
        "organic": organic_data,
        "offline": offline_data,
    }, None