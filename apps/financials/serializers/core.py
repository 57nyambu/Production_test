from rest_framework import serializers
from django.db import transaction
from django.core.exceptions import ValidationError

from django.db import models
class BaseModelSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'created_at', 'updated_at']  # Changed to list instead of tuple
        read_only_fields = ['id', 'created_at', 'updated_at']

    def _inject_user(self, validated_data):
        """Inject the authenticated user into the validated data."""
        current_user = self.context['request'].user
        if current_user.is_anonymous:
            raise ValidationError("User must be authenticated to perform this action.")
        validated_data['user'] = current_user
        return validated_data

    def create(self, validated_data):
        """Override create method to inject the user."""
        validated_data = self._inject_user(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Override update method to inject the user."""
        validated_data = self._inject_user(validated_data)
        return super().update(instance, validated_data)
    

class NestedManyToManyMixin(serializers.ModelSerializer):
    def _get_unique_fields(self, model):
        """Get unique fields for the model, defaulting to ('id',) if not defined."""
        if model._meta.unique_together:
            return model._meta.unique_together[0]
        return ('id',)

    def _generate_lookup_key(self, item, unique_fields):
        """Generate a lookup key for the item based on unique_fields."""
        key = []
        for field in unique_fields:
            value = item.get(field)
            if isinstance(value, models.Model):
                key.append(value.id)
            else:
                key.append(value)
        return tuple(key)

    def _bulk_get_or_create_related(self, model, data_list):
        """Bulk get or create related objects."""
        unique_fields = self._get_unique_fields(model)
        lookup_dict = {}
        
        # Generate lookup keys for each item in the data_list
        for item in data_list:
            key = self._generate_lookup_key(item, unique_fields)
            lookup_dict[key] = item
            
        # Filter existing objects by unique fields
        existing = model.objects.filter(
            **{f"{field}__in": [item.get(field) for item in data_list] for field in unique_fields}
        )
        
        # Create a set of keys for existing objects
        found_keys = set(self._generate_lookup_key(obj, unique_fields) for obj in existing)
        
        # Prepare objects to create
        to_create = [
            model(**lookup_dict[key])
            for key in lookup_dict.keys() - found_keys
        ]
        
        # Bulk create new objects
        if to_create:
            existing = list(existing) + model.objects.bulk_create(to_create)
            
        return existing

    @transaction.atomic
    def create(self, validated_data):
        """Create an instance with nested many-to-many relationships."""
        nested_fields = {
            field_name: validated_data.pop(field_name, [])
            for field_name in self.nested_many_to_many_fields
        }
        
        # Create the instance using the parent class's create method
        instance = super().create(validated_data)
        
        # Handle nested many-to-many fields
        for field_name, related_data in nested_fields.items():
            if not related_data:
                continue
                
            related_model = self.fields[field_name].child.Meta.model
            related_objects = self._bulk_get_or_create_related(related_model, related_data)
            getattr(instance, field_name).set(related_objects)
            
        return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        """Update an instance with nested many-to-many relationships."""
        nested_fields = {
            field_name: validated_data.pop(field_name, [])
            for field_name in self.nested_many_to_many_fields
        }
        
        # Update the instance using the parent class's update method
        instance = super().update(instance, validated_data)
        
        # Handle nested many-to-many fields
        for field_name, related_data in nested_fields.items():
            if not related_data:
                continue
                
            related_model = self.fields[field_name].child.Meta.model
            related_objects = self._bulk_get_or_create_related(related_model, related_data)
            getattr(instance, field_name).set(related_objects)
            
        return instance