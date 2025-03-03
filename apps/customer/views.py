from .models import CustomerModel, CustomerPercentageDistribution
from .serializers import CustomerModelSerializer, CustomerPercentageDistributionSerializer
from apps.utils.baseViews import BaseAPIView

class CustomerModelView(BaseAPIView):
    model = CustomerModel
    serializer_class = CustomerModelSerializer


class CustomerPercentageDistributionView(BaseAPIView):
    model = CustomerPercentageDistribution
    serializer_class = CustomerPercentageDistributionSerializer
