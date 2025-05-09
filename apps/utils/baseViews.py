from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.core.exceptions import ImproperlyConfigured
from rest_framework.permissions import IsAuthenticated

class BaseAPIView(APIView):
    """Base API View that ensures:
    - Resources are created only once per user (switches to PATCH if they exist).
    - Works seamlessly with BaseCombinedSerializer.
    - Provides standardized response format with success, message, and data.
    """
    model = None
    serializer_class = None
    permission_classes = [IsAuthenticated]
    
    def get_instance(self, request):
        """Retrieve the user's instance if it exists, otherwise return None."""
        if not self.model:
            raise ImproperlyConfigured("Model must be defined")
        
        return self.model.objects.filter(user=request.user).first()
    
    def format_response(self, data=None, message="", success=True, status_code=status.HTTP_200_OK):
        """Format standardized API response."""
        response = {
            "success": success,
            "message": message,
            "data": data or {}
        }
        return Response(response, status=status_code)
    
    def get(self, request, *args, **kwargs):
        """Retrieve existing instance data."""
        instance = self.get_instance(request)
        if not instance:
            return self.format_response(
                message="No data found", 
                success=False,
                status_code=status.HTTP_404_NOT_FOUND
            )

        serializer = self.serializer_class(instance, context={'request': request})
        return self.format_response(
            data=serializer.data,
            message="Data retrieved successfully",
            success=True
        )

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """Create new resource or update if it exists."""
        instance = self.get_instance(request)

        if instance:
            # If instance exists, switch to PATCH
            return self.patch(request, *args, **kwargs)

        serializer = self.serializer_class(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return self.format_response(
                data={"errors": serializer.errors},
                message="Validation error",
                success=False,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        # This will use the BaseCombinedSerializer's create method which 
        # handles nested relationships through _handle_nested_relations
        instance = serializer.save(user=request.user)

        return self.format_response(
            data=serializer.data,
            message="Data created successfully",
            success=True,
            status_code=status.HTTP_201_CREATED
        )

    @transaction.atomic
    def patch(self, request, *args, **kwargs):
        """Update existing resource."""
        instance = self.get_instance(request)
        if not instance:
            return self.format_response(
                message="Instance not found",
                success=False,
                status_code=status.HTTP_404_NOT_FOUND
            )

        serializer = self.serializer_class(
            instance, 
            data=request.data, 
            partial=True, 
            context={'request': request}
        )
        if not serializer.is_valid():
            return self.format_response(
                data={"errors": serializer.errors},
                message="Validation error",
                success=False,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        # This will use the BaseCombinedSerializer's update method which 
        # handles nested relationships through _handle_nested_relations
        instance = serializer.save()

        return self.format_response(
            data=serializer.data,
            message="Data updated successfully",
            success=True
        )
            
    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        """Delete entire resource or nested related items based on payload."""
        instance = self.get_instance(request)
        if not instance:
            return self.format_response(
                message="Instance not found",
                success=False,
                status_code=status.HTTP_404_NOT_FOUND
            )

        # If no payload, delete the whole main instance
        if not request.data:
            instance.delete()
            return self.format_response(
                message="Data deleted successfully",
                success=True
            )

        # Delete nested items based on payload keys and IDs
        errors = []
        for field_name, ids in request.data.items():
            field = getattr(instance, field_name, None)
            if not field or not hasattr(field, "model"):
                errors.append(f"Invalid field: {field_name}")
                continue

            related_model = field.model
            user = request.user

            for obj_id in ids:
                try:
                    related_instance = related_model.objects.get(id=obj_id, user=user)
                    field.remove(related_instance)  # For many-to-many
                    related_instance.delete()      # If you want to delete the object itself
                except related_model.DoesNotExist:
                    errors.append(f"{field_name} id {obj_id} not found")

        if errors:
            return self.format_response(
                message="Partial deletion with some errors",
                data={"errors": errors},
                success=False,
                status_code=status.HTTP_207_MULTI_STATUS
            )

        return self.format_response(
            message="Nested items deleted successfully",
            success=True
        )



class BaseReadOnlyView(APIView):
    """Base view to handle read-only operations for models with the provided serializer."""
    permission_classes = [IsAuthenticated]
    serializer_class = None
    model_class = None

    def get(self, request, *args, **kwargs):
        """Handle GET request for read-only views."""
        try:
            instance = self.model_class.objects.filter(user=request.user).first()

            if not instance:
                return Response(
                    {"success": False, "error": f"No data found for {self.model_class.__name__}."},
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = self.serializer_class(instance)

            return Response(
                {"success": True, "data": [serializer.data]},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )