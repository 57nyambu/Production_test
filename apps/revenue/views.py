from .models import RevenueModel
from .serializers import RevenueModelSerializer,RevenueStreamsSerializer, RevenueStream
from apps.utils.baseViews import BaseAPIView, GenericCombinedView


class RevenueView(BaseAPIView):
    model = RevenueModel
    serializer_class = RevenueModelSerializer

class RevenueStreamView(GenericCombinedView):
    model_class = RevenueStream
    serializer_class = RevenueStreamsSerializer

