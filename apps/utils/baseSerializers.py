from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.db import models
from django.db import transaction

class BaseModelSerializer():
    pass

class BaseCombinedSerializer(serializers.ModelSerializer):
    """Base serializer to handle nested and many-to-many relationships."""

    class Meta:
        abstract = True
        fields = ['id', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def _handle_nested_relations(self, instance, validated_data, partial=False):
        """Handles Many-to-Many and ForeignKey nested relations properly.
        
        When partial=True (for PATCH requests), items will be added rather than replaced.
        """
        user = self.context["request"].user  # Get authenticated user

        for field_name, value in validated_data.items():
            field = self.fields.get(field_name)

            if isinstance(field, serializers.ListSerializer) and isinstance(field.child, serializers.ModelSerializer):
                # Handling Many-to-Many Relationship
                model_class = field.child.Meta.model
                related_instances = []

                for item in value:
                    item["user"] = user  # Inject user
                    
                    # If the item has an ID and we're in partial mode, try to update it
                    if partial and 'id' in item and item['id']:
                        try:
                            obj = model_class.objects.get(id=item['id'], user=user)
                            # Update existing object
                            for attr, attr_value in item.items():
                                if attr != 'id' and attr != 'user':  # Don't change id and user
                                    setattr(obj, attr, attr_value)
                            obj.save()
                        except model_class.DoesNotExist:
                            # If ID specified doesn't exist, create new
                            obj = model_class.objects.create(**item)
                    else:
                        # For new items (no ID or not in partial mode)
                        obj = model_class.objects.filter(**item).first()  # Get first match if it exists
                        if not obj:
                            obj = model_class.objects.create(**item)  # Create if not found
                            
                    related_instances.append(obj)

                if partial:
                    # In partial mode (PATCH), add to existing instead of replacing
                    current_items = list(getattr(instance, field_name).all())
                    
                    # Only add items that aren't already in the relation
                    # by comparing IDs to avoid duplicates
                    existing_ids = [item.id for item in current_items]
                    new_items = [item for item in related_instances if item.id not in existing_ids]
                    
                    # Add the new items to the existing ones
                    getattr(instance, field_name).add(*new_items)
                else:
                    # In full mode (POST), replace all items
                    getattr(instance, field_name).set(related_instances)

            elif isinstance(field, serializers.ModelSerializer):
                # Handling ForeignKey Relationship
                model_class = field.Meta.model
                value["user"] = user  # Inject user
                
                if partial and getattr(instance, field_name) is not None:
                    # In partial mode with existing relation, update it
                    obj = getattr(instance, field_name)
                    for attr, attr_value in value.items():
                        if attr != 'id' and attr != 'user':  # Don't change id and user
                            setattr(obj, attr, attr_value)
                    obj.save()
                else:
                    # Create new related object
                    obj = model_class.objects.filter(**value).first()  # Get first match if it exists
                    if not obj:
                        obj = model_class.objects.create(**value)  # Create if not found
                    setattr(instance, field_name, obj)

    @transaction.atomic
    def create(self, validated_data):
        """Generic create method supporting nested Many-to-Many and ForeignKey fields."""
        nested_data = {key: validated_data.pop(key) for key in list(validated_data.keys()) if isinstance(self.fields.get(key), (serializers.ListSerializer, serializers.ModelSerializer))}
        
        instance = self.Meta.model.objects.create(**validated_data)  # Create main instance

        self._handle_nested_relations(instance, nested_data, partial=False)  # Handle nested relations

        return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        """Generic update method supporting nested Many-to-Many and ForeignKey fields."""
        nested_data = {key: validated_data.pop(key) for key in list(validated_data.keys()) if isinstance(self.fields.get(key), (serializers.ListSerializer, serializers.ModelSerializer))}
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()

        self._handle_nested_relations(instance, nested_data, partial=True)  # Handle nested relations with partial=True

        return instance