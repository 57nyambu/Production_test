from rest_framework import serializers
from django.db import transaction
from rest_framework.exceptions import ValidationError

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


class BaseCombinedSerializer(serializers.Serializer):
    """Base class to handle combined serializers dynamically."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._propagate_context(kwargs.get("context", {}))

    def _propagate_context(self, context):
        """Propagate context to all nested serializers."""
        for field in self.fields.values():
            if isinstance(field, serializers.BaseSerializer):
                field.context.update(context)

    def _inject_user(self, data):
        """Inject user into data recursively."""
        request = self.context.get("request")
        if not request or request.user.is_anonymous:
            raise serializers.ValidationError("Authentication required")

        user = request.user

        def inject_user_recursive(data_dict):
            if isinstance(data_dict, dict):
                data_dict["user"] = user
                for value in data_dict.values():
                    if isinstance(value, (dict, list)):
                        inject_user_recursive(value)
            elif isinstance(data_dict, list):
                for item in data_dict:
                    if isinstance(item, (dict, list)):
                        inject_user_recursive(item)
            return data_dict

        return inject_user_recursive(data.copy())

    def _get_model_and_serializer(self, key):
        """Get model class and serializer instance."""
        serializer = self.fields[key]
        model_class = getattr(serializer.child.Meta, "model", None) if hasattr(serializer, "child") else getattr(serializer.Meta, "model", None)
        return model_class, serializer

    def _handle_nested_data(self, data):
        """Split data into regular and nested fields."""
        regular_data = {}
        nested_data = {}

        for field_name, value in data.items():
            if isinstance(value, list):
                nested_data[field_name] = value
            elif field_name != "user":
                regular_data[field_name] = value

        if "user" in data:
            regular_data["user"] = data["user"]

        return regular_data, nested_data

    def _create_nested_instances(self, nested_data, model_class, user):
        """Create nested model instances."""
        return [model_class.objects.create(user=user, **item) for item in nested_data]

    @transaction.atomic
    def create(self, validated_data):
        """Create main and nested instances dynamically."""
        instances = {}
        user = self.context["request"].user

        for key, data in validated_data.items():
            if not data:
                continue

            model_class, serializer = self._get_model_and_serializer(key)
            regular_data, nested_data = self._handle_nested_data(data)

            instance = model_class.objects.create(**regular_data)

            for field_name, items in nested_data.items():
                nested_model = serializer.fields[field_name].child.Meta.model
                related_instances = self._create_nested_instances(items, nested_model, user)
                getattr(instance, field_name).set(related_instances)

            instances[key] = instance

        return instances

    @transaction.atomic
    def update(self, instance_mapping, validated_data):
        """Update main and nested instances dynamically."""
        updated_instances = {}
        user = self.context["request"].user

        for key, data in validated_data.items():
            if not data:
                continue

            instance = instance_mapping.get(key)
            if not instance:
                continue

            model_class, serializer = self._get_model_and_serializer(key)
            regular_data, nested_data = self._handle_nested_data(data)

            for field_name, value in regular_data.items():
                if field_name != "user":
                    setattr(instance, field_name, value)

            for field_name, items in nested_data.items():
                related_field = getattr(instance, field_name)
                related_field.all().delete()

                nested_model = serializer.fields[field_name].child.Meta.model
                related_instances = self._create_nested_instances(items, nested_model, user)
                related_field.set(related_instances)

            instance.save()
            updated_instances[key] = instance

        return updated_instances
