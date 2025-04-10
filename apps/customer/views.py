from .models import CustomerModel
from apps.marketing.models import GrowthRate
from .serializers import CustomerModelSerializer
from apps.utils.baseViews import BaseAPIView, BaseGetAPIView, GenericCombinedView

class CustomerModelView(BaseAPIView):
    model = CustomerModel
    serializer_class = CustomerModelSerializer


class GrowthRateView1(BaseGetAPIView):
    model = CustomerModel
    serializer_class = GrowthRate

