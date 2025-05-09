from rest_framework import serializers
from django.db import transaction


class BaseCombinedSerializer(serializers.ModelSerializer):
    """Base serializer to handle nested and many-to-many relationships."""

    class Meta:
        abstract = True
        fields = ['id', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


    def to_representation(self, instance):
        """Customize response to exclude `id` and `created_at`."""
        data = super().to_representation(instance)
        
        # Remove unwanted fields
        data.pop("created_at", None)
        # Recursively clean nested fields (Many-to-Many & ForeignKey)
        for field_name, field_value in data.items():
            if isinstance(field_value, list):
                data[field_name] = [
                    {k: v for k, v in item.items() if k not in ["created_at"]}
                    for item in field_value
                ]
            elif isinstance(field_value, dict):
                data[field_name] = {k: v for k, v in field_value.items() if k not in ["created_at"]}

        return data


    def _handle_nested_relations(self, instance, validated_data, partial=False):
        """Handles nested Many-to-Many and ForeignKey relations with smart update-or-create logic."""
        user = self.context["request"].user

        for field_name, value in validated_data.items():
            field = self.fields.get(field_name)

            if isinstance(field, serializers.ListSerializer) and isinstance(field.child, serializers.ModelSerializer):
                # Many-to-Many relationship
                model_class = field.child.Meta.model
                related_instances = []

                for item in value:
                    item["user"] = user
                    obj = None

                    # Try update by ID
                    if "id" in item:
                        try:
                            obj = model_class.objects.get(id=item["id"], user=user)
                            for attr, attr_value in item.items():
                                if attr not in ["id", "user"]:
                                    setattr(obj, attr, attr_value)
                            obj.save()
                        except model_class.DoesNotExist:
                            obj = None

                    # Try match by unique fields if no valid ID or not found
                    if obj is None:
                        lookup_fields = ["name", "type", "user"]  # adjust for each model if needed
                        lookup = {k: item[k] for k in lookup_fields if k in item}
                        obj = model_class.objects.filter(**lookup).first()

                        if obj:
                            for attr, attr_value in item.items():
                                if attr not in ["id", "user"]:
                                    setattr(obj, attr, attr_value)
                            obj.save()
                        else:
                            obj = model_class.objects.create(**item)

                    related_instances.append(obj)

                if partial:
                    current_items = list(getattr(instance, field_name).all())
                    existing_ids = [item.id for item in current_items]
                    new_items = [item for item in related_instances if item.id not in existing_ids]
                    getattr(instance, field_name).add(*new_items)
                else:
                    getattr(instance, field_name).set(related_instances)

            elif isinstance(field, serializers.ModelSerializer):
                # ForeignKey relationship
                model_class = field.Meta.model
                value["user"] = user
                obj = None

                if partial and getattr(instance, field_name) is not None:
                    obj = getattr(instance, field_name)
                    for attr, attr_value in value.items():
                        if attr not in ["id", "user"]:
                            setattr(obj, attr, attr_value)
                    obj.save()
                else:
                    lookup_fields = ["name", "type", "user"]
                    lookup = {k: value[k] for k in lookup_fields if k in value}
                    obj = model_class.objects.filter(**lookup).first()
                    if obj:
                        for attr, attr_value in value.items():
                            if attr not in ["id", "user"]:
                                setattr(obj, attr, attr_value)
                        obj.save()
                    else:
                        obj = model_class.objects.create(**value)

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