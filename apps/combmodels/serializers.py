from rest_framework import serializers
from django.db import models
from .models import (Marketing, 
                     Customer, 
                     Revenue, 
                     Operation)


class BaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = None
        fields = ['id', 'user', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

        