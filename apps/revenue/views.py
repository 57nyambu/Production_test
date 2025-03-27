from .models import RevenueModel
from .serializers import RevenueModelSerializer
from apps.utils.baseViews import BaseAPIView


class RevenueView(BaseAPIView):
    model = RevenueModel
    serializer_class = RevenueModelSerializer
