from apps.utils.baseViews import BaseModelAPIView
from .serializers import (
    MarketingCostSerializer,
    CustomerAcquisitionSerializer,
    GrowthRateSerializer,
    ClientSegmentSerializer,
    CustomerAcquisitionCostSerializer,
    CombinedMarketSerializer
)
from .models import (
    MarketingCost,
    CustomerAcquisition,
    GrowthRate,
    ClientSegment,
    CustomerAcquisitionCost
)

class MarketingCostView(BaseModelAPIView):
    serializer_class = MarketingCostSerializer
    model = MarketingCost

class CombinedMarketView(BaseModelAPIView):
    pass