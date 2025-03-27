from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.core.exceptions import ImproperlyConfigured
from rest_framework.permissions import IsAuthenticated
from typing import Type, Dict, Any, Callable

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
    

class BaseGetAPIView(APIView):
    """
    Base API View that ensures:
    - Standardized GET response format.
    - Works with both single and multiple records.
    - Provides success, message, and data fields in the response.
    """
    model = None
    serializer_class = None
    permission_classes = [IsAuthenticated]

    def get_queryset(self, request):
        """
        Override this method in child views to return multiple records if needed.
        Default: Returns only the first instance for the logged-in user.
        """
        if not self.model:
            raise ImproperlyConfigured("Model must be defined")
        
        return self.model.objects.filter(user=request.user)

    def format_response(self, data=None, message="", success=True, status_code=status.HTTP_200_OK):
        """Format standardized API response."""
        return Response({
            "success": success,
            "message": message,
            "data": data if data else {}
        }, status=status_code)

    def get(self, request, *args, **kwargs):
        """Retrieve instance(s) based on the queryset."""
        queryset = self.get_queryset(request)

        if not queryset.exists():
            return self.format_response(
                message="No data found", 
                success=False, 
                status_code=status.HTTP_404_NOT_FOUND
            )

        serializer = self.serializer_class(queryset, many=queryset.count() > 1, context={'request': request})
        return self.format_response(
            data=serializer.data,
            message="Data retrieved successfully",
            success=True
        )


class GenericCombinedView(APIView):
    """
    A highly flexible and easy-to-use API view for combining multiple serializers.
    
    Simplified Usage:
    class MyCombinedView(GenericCombinedView):
        class Meta:
            serializers = {
                'users': UserSerializer,
                'profiles': ProfileSerializer
            }
            # Optional configurations
            queries = {
                'users': lambda: User.objects.filter(is_active=True)
            }
            transforms = {
                'profiles': lambda data: [p for p in data if p['is_premium']]
            }
    """
    permission_classes = [IsAuthenticated]

    def get_serialized_data(self, serializer_class: Type, queryset=None) -> Any:
        """
        Serialize data for a given serializer class.
        
        :param serializer_class: Serializer class to use
        :param queryset: Optional queryset to serialize
        :return: Serialized data
        """
        try:
            # Handle ModelSerializer
            if hasattr(serializer_class, 'Meta') and hasattr(serializer_class.Meta, 'model'):
                # Use provided queryset or fetch all
                queryset = queryset or serializer_class.Meta.model.objects.all()
                serializer = serializer_class(queryset, many=True)
            else:
                # For non-model serializers
                serializer = serializer_class()
            
            return serializer.data
        except Exception as e:
            return {
                'error': str(e),
                'data': None
            }

    def get(self, request, *args, **kwargs):
        """
        Retrieve and combine data from multiple serializers.
        """
        try:
            # Validate Meta class exists
            if not hasattr(self, 'Meta'):
                raise AttributeError("View must define a Meta class with serializers")

            # Get serializers from Meta
            serializers = getattr(self.Meta, 'serializers', {})
            if not serializers:
                raise ValueError("No serializers defined in Meta.serializers")

            # Prepare combined data
            combined_data = {}

            # Process each serializer
            for key, serializer_class in serializers.items():
                # Get custom query if defined
                query_method = getattr(
                    self.Meta, 
                    'queries', 
                    {}
                ).get(key)
                
                # Get queryset from custom method or use default
                queryset = query_method() if query_method else None
                
                # Serialize data
                serialized_data = self.get_serialized_data(serializer_class, queryset)
                
                # Apply optional data transformation
                transform_method = getattr(
                    self.Meta, 
                    'transforms', 
                    {}
                ).get(key)
                
                if transform_method:
                    serialized_data = transform_method(serialized_data)
                
                # Store in combined data
                combined_data[key] = serialized_data

            # Return successful response
            return Response({
                "success": True,
                "message": "Data retrieved successfully",
                "data": combined_data
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            # Handle any unexpected errors
            return Response({
                "success": False,
                "message": f"Error retrieving data: {str(e)}",
                "data": {}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)