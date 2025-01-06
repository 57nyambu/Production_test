from django.urls import path
#from rest_framework.documentation import include_docs_urls
from .views import CombinedCreateUpdateAPIView


urlpatterns = [
    # Main endpoint for all combined data operations (GET, POST, PUT)
    path(
        'combined-resource/',  # Clean, descriptive URL
        CombinedCreateUpdateAPIView.as_view(),
        name='combined-resource'
    )
]