from apps.financials.views import SmartModelViewSet
from .serializers import MarketingSerializer
from .models import Marketing

class MarketingViewSet(SmartModelViewSet):
    serializer_class = MarketingSerializer
    queryset = Marketing.objects.all()

