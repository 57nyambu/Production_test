from .models import Emails
from .serializers import EmailRequestSerializer, EmailsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.utils.emailService import modelGuide


class EmailsAPIView(APIView):
    def post(self, request):
        serializer = EmailRequestSerializer(data=request.data)
        if serializer.is_valid():
            email_obj = serializer.save()  # Save first
        
            modelGuide(email_obj.email)  # Pass only the email string

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailsListAPIView(APIView):
    def get(self, request):
        emails = Emails.objects.all()
        serializer = EmailsSerializer(emails, many=True)
        return Response(serializer.data)