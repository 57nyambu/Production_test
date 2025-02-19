from apps.financials.views import BaseModelAPIView
from .serializers import MarketingSerializer
from .models import Marketing

class MarketingAPIView(BaseModelAPIView):
    serializer_class = MarketingSerializer
    model = Marketing

