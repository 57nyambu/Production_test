from apps.financials.views import BaseAPIView
from .serializers import MarketingSerializer
from .models import Marketing

class MarketingAPIView(BaseAPIView):
    serializer_class = MarketingSerializer
    model_class = Marketing

