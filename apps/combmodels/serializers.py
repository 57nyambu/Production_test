from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.db import transaction
from apps.financials.serializers import BaseModelSerializer
from .models import (MarketingType,
                    Marketing, 
                     Customer, 
                     Revenue, 
                     Operation)

class MarketingTypeSerializer(BaseModelSerializer):
    class Meta:
        model = MarketingType
        fields = fields = BaseModelSerializer.Meta.fields +[
            'name', 'cost']


class MarketingSerializer(BaseModelSerializer):
    market_type = MarketingTypeSerializer(many=True, required=False)
    class Meta:
        model = Marketing
        fields = fields = BaseModelSerializer.Meta.fields +[
            'market_type', 'monthly_market_cost', 'yearly_market_cost', 'cust_acq_cost',
              'subscript_count', 'subscript_dist', 'growth_rate']
        

class CombinedSerializer(serializers.Serializer):
    marketing_serializer = MarketingSerializer(required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._propagate_context(kwargs.get('context', {}))

    def _propagate_context(self, context):
        """Propagate context to nested serializers."""
        for field in self.fields.values():
            if isinstance(field, serializers.BaseSerializer):
                field.context.update(context)

    def _inject_user(self, data):
        """Inject user into data structure recursively."""
        if not self.context.get('request'):
            raise serializers.ValidationError("Request context is required")
            
        user = self.context['request'].user
        if user.is_anonymous:
            raise serializers.ValidationError("Authentication required")

        def inject_user_recursive(data_dict):
            if isinstance(data_dict, dict):
                data_dict['user'] = user
                for value in data_dict.values():
                    if isinstance(value, (dict, list)):
                        inject_user_recursive(value)
            elif isinstance(data_dict, list):
                for item in data_dict:
                    if isinstance(item, (dict, list)):
                        inject_user_recursive(item)
            return data_dict

        return inject_user_recursive(data.copy())  # Work on a copy to prevent modifying original data

    def to_internal_value(self, data):
        """Convert and validate input data."""
        validated_data = super().to_internal_value(data)
        return self._inject_user(validated_data)

    def _get_model_and_serializer(self, key):
        """Get model class and serializer instance."""
        serializer = self.fields[key]
        if hasattr(serializer, 'child'):
            model_class = serializer.child.Meta.model
        else:
            model_class = serializer.Meta.model
        return model_class, serializer

    def _handle_nested_data(self, data):
        """Split data into regular and nested fields."""
        regular_data = {}
        nested_data = {}
        
        for field_name, value in data.items():
            if isinstance(value, list):
                nested_data[field_name] = value
            elif field_name != 'user':  # Preserve user field
                regular_data[field_name] = value
                
        if 'user' in data:
            regular_data['user'] = data['user']
            
        return regular_data, nested_data

    def _create_nested_instances(self, nested_data, model_class, user):
        """Create nested model instances."""
        instances = []
        for item in nested_data:
            item['user'] = user
            instances.append(model_class.objects.create(**item))
        return instances

    @transaction.atomic
    def create(self, validated_data):
        """Create main and nested instances."""
        instances = {}
        try:
            user = self.context['request'].user
            
            for key, data in validated_data.items():
                if not data:
                    continue
                    
                model_class, serializer = self._get_model_and_serializer(key)
                regular_data, nested_data = self._handle_nested_data(data)
                
                # Create main instance
                instance = model_class.objects.create(**regular_data)
                
                # Handle nested relationships
                for field_name, items in nested_data.items():
                    nested_model = serializer.fields[field_name].child.Meta.model
                    related_instances = self._create_nested_instances(items, nested_model, user)
                    getattr(instance, field_name).set(related_instances)
                
                instances[key] = instance
                
            return instances
            
        except Exception as e:
            raise serializers.ValidationError(f"Creation failed: {str(e)}")

    @transaction.atomic
    def update(self, instance_mapping, validated_data):
        """Update main and nested instances."""
        updated_instances = {}
        try:
            user = self.context['request'].user
            
            for key, data in validated_data.items():
                if not data:
                    continue
                    
                instance = instance_mapping.get(key)
                if not instance:
                    continue
                    
                model_class, serializer = self._get_model_and_serializer(key)
                regular_data, nested_data = self._handle_nested_data(data)
                
                # Update regular fields
                for field_name, value in regular_data.items():
                    if field_name != 'user':  # Prevent user modification
                        setattr(instance, field_name, value)
                
                # Update nested relationships
                for field_name, items in nested_data.items():
                    related_field = getattr(instance, field_name)
                    related_field.all().delete()  # Clear existing relations
                    
                    nested_model = serializer.fields[field_name].child.Meta.model
                    related_instances = self._create_nested_instances(items, nested_model, user)
                    related_field.set(related_instances)
                
                instance.save()
                updated_instances[key] = instance
                
            return updated_instances
            
        except Exception as e:
            raise serializers.ValidationError(f"Update failed: {str(e)}")
