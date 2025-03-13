from .models import Emails
from .serializers import EmailRequestSerializer, EmailsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.utils.emailService import modelGuide


from datetime import datetime

class NotificationView(APIView):
    def get(self, request):
        latest_notification = {
            'message': 'New feature available!',
            'timestamp': datetime.now().isoformat()
        }
        return Response(latest_notification)

class EmailsAPIView(APIView):
    def post(self, request):
        serializer = EmailRequestSerializer(data=request.data)
        if serializer.is_valid():
            email_data = serializer.validated_data  # Save first
            modelGuide(email_data['email'])
            email_data = serializer.save()

            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_200_OK)


class EmailsListAPIView(APIView):
    def get(self, request):
        emails = Emails.objects.all()
        serializer = EmailsSerializer(emails, many=True)
        return Response(serializer.data)