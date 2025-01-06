from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import CombinedSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics
from apps.subscriptions.permissions import HasActiveSubscription
from rest_framework.exceptions import ValidationError
from django.db import transaction
from typing import Dict, Any


class CombinedCreateUpdateAPIView(generics.GenericAPIView):
    """
    Enhanced endpoint for creating, updating, and retrieving combined model data.
    Implements atomic transactions and efficient database queries.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CombinedSerializer
    
    # Response messages as class constants
    MESSAGES = {
        'created': "Data saved successfully.",
        'updated': "Data updated successfully.",
        'fetched': "Data fetched successfully.",
        'exists': "Resource already exists. Use PUT to update the resource.",
        'failed': "Operation failed.",
    }

    def get_queryset(self):
        """
        Get queryset for all related models in a single database query.
        """
        return {
            model_key: self.serializer_class._declared_fields[model_key].Meta.model.objects.filter(
                user=self.request.user
            )
            for model_key in self.serializer_class._declared_fields
        }

    def create_response(self, success: bool, message: str, data: Any = None, 
                       status_code: int = status.HTTP_200_OK) -> Response:
        """
        Standardized response creation method.
        """
        return Response(
            {
                'success': success,
                'message': message,
                'data': data,
            },
            status=status_code
        )

    def get(self, request, *args, **kwargs) -> Response:
        """
        Efficiently fetch existing instance data for all models using select_related.
        """
        try:
            instance_mapping = {
                key: queryset.select_related().first()
                for key, queryset in self.get_queryset().items()
            }
            serializer = self.get_serializer(instance_mapping)
            return self.create_response(True, self.MESSAGES['fetched'], serializer.data)
        except Exception as e:
            return self.create_response(
                False, 
                f"Error fetching data: {str(e)}", 
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def resource_exists(self) -> bool:
        """
        Efficiently check resource existence using exists() query.
        """
        return any(
            queryset.exists()
            for queryset in self.get_queryset().values()
        )

    @transaction.atomic
    def post(self, request, *args, **kwargs) -> Response:
        """
        Handle create operation with atomic transaction.
        """
        if self.resource_exists():
            return self.create_response(
                False,
                self.MESSAGES['exists'],
                status_code=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=self.prepare_data(request.data))
        
        try:
            if not serializer.is_valid():
                return self.create_response(
                    False,
                    self.MESSAGES['failed'],
                    serializer.errors,
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            instance_mapping = serializer.save()
            response_data = {
                'modelIds': {
                    key: str(instance.id) 
                    for key, instance in instance_mapping.items()
                },
                **serializer.data
            }
            return self.create_response(
                True,
                self.MESSAGES['created'],
                response_data,
                status_code=status.HTTP_201_CREATED
            )

        except ValidationError as e:
            return self.create_response(
                False,
                str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return self.create_response(
                False,
                f"Unexpected error: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @transaction.atomic
    def put(self, request, *args, **kwargs) -> Response:
        """
        Handle update operation with atomic transaction.
        """
        try:
            instance_mapping = {
                key: queryset.select_for_update().first()
                for key, queryset in self.get_queryset().items()
            }
            
            if not any(instance_mapping.values()):
                return self.create_response(
                    False,
                    "No resources found to update.",
                    status_code=status.HTTP_404_NOT_FOUND
                )

            serializer = self.get_serializer(
                instance_mapping,
                data=self.prepare_data(request.data),
                partial=kwargs.get('partial', False)
            )

            if not serializer.is_valid():
                return self.create_response(
                    False,
                    self.MESSAGES['failed'],
                    serializer.errors,
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            serializer.save()
            return self.create_response(True, self.MESSAGES['updated'], serializer.data)

        except ValidationError as e:
            return self.create_response(
                False,
                str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return self.create_response(
                False,
                f"Unexpected error: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def prepare_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        prepared_data = data.copy()
        user_id = self.request.user.id
        
        prepared_data['user'] = user_id
        
        for key, field in self.serializer_class._declared_fields.items():
            if isinstance(prepared_data.get(key), dict):
                prepared_data[key]['user'] = user_id
                
        return prepared_data