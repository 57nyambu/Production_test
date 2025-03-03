from .models import MarketingMetrics
from .serializers import MarketingMetricsSerializer
from apps.utils.baseViews import BaseAPIView

class MarketingMetricsView(BaseAPIView):
    """View to handle Marketing Metrics API requests."""
    model = MarketingMetrics
    serializer_class = MarketingMetricsSerializer
