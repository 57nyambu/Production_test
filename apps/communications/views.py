from .models import RecievedEmails, Emails
from .serializers import RecievedEmailsSerializer, EmailsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.utils.emailService import modelGuide

class RecievedEmailsAPIView(APIView):
    def get(self, request):
        emails = RecievedEmails.objects.all()
        serializer = RecievedEmailsSerializer(emails, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RecievedEmailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class EmailsAPIView(APIView):
    def get(self, request):
        emails = Emails.objects.all()
        serializer = EmailsSerializer(emails, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        user_email = request.data
        serializer = EmailsSerializer(data=user_email)
        if serializer.is_valid():
            modelGuide(user_email)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        email = Emails.objects.get(pk=pk)
        serializer = EmailsSerializer(email, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        email = Emails.objects.get(pk=pk)
        email.delete() 
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def patch(self, request, pk):
        email = Emails.objects.get(pk=pk)
        serializer = EmailsSerializer(email, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
