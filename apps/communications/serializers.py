from rest_framework import serializers
from .models import RecievedEmails, Emails

class RecievedEmailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecievedEmails
        fields = ['email', 'sender', 'subject'] 


class EmailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emails 
        fields = ['email', 'type']
