from rest_framework import serializers
from .models.company import CompanyInformation
from .models.financials import FinancialModel

class CompanyInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyInformation
        fields = '__all__'

class FinancialModelSerializer(serializers.ModelSerializer):
    company = CompanyInformationSerializer()  # Nested serializer

    class Meta:
        model = FinancialModel
        fields = '__all__'
