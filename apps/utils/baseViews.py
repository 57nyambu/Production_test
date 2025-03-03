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
        """Delete existing resource."""
        instance = self.get_instance(request)
        if not instance:
            return self.format_response(
                message="Instance not found",
                success=False,
                status_code=status.HTTP_404_NOT_FOUND
            )
            
        instance.delete()
        
        return self.format_response(
            message="Data deleted successfully",
            success=True
        )