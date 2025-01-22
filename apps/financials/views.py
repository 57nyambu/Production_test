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
import logging

logger = logging.getLogger(__name__)


class CombinedCreateUpdateAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CombinedSerializer

    def get_queryset(self):
        return {
            field_name: field.Meta.model.objects.filter(
                user=self.request.user
            ).select_related('user').prefetch_related(
                *self._get_prefetch_fields(field)
            )
            for field_name, field in self.get_serializer().fields.items()
        }

    def _get_prefetch_fields(self, field):
        prefetch_fields = []
        if hasattr(field, 'child'):
            meta = getattr(field.child, 'Meta', None)
        else:
            meta = getattr(field, 'Meta', None)
            
        if meta and hasattr(meta, 'model'):
            for related_field in meta.model._meta.get_fields():
                if related_field.is_relation:
                    prefetch_fields.append(related_field.name)
        
        return prefetch_fields

    def _get_all_data(self):
        instances = {
            key: queryset.first()
            for key, queryset in self.get_queryset().items()
        }
        serializer = self.get_serializer(instances)
        return serializer.data

    def get(self, request, *args, **kwargs):
        try:
            data = self._get_all_data()
            return Response({
                'success': True,
                'message': "Data retrieved successfully",
                'data': data
            })
        except Exception as e:
            return Response({
                'success': False,
                'message': f"Error retrieving data: {str(e)}",
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """POST method with redirect to PATCH if resources exist"""
        try:
            # Check for existing resources
            existing_resources = {
                key: self.get_queryset()[key].exists()
                for key in request.data.keys()
            }

            # If any requested resource exists, redirect to PATCH
            if any(existing_resources.values()):
                existing_keys = [k for k, v in existing_resources.items() if v]
                return Response({
                    'success': False,
                    'message': f"Resources already exist for: {', '.join(existing_keys)}. Use PATCH to update.",
                    'data': self._get_all_data()
                }, status=status.HTTP_409_CONFLICT)

            serializer = self.get_serializer(
                data=request.data,
                context={'request': request}
            )

            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': "Validation failed",
                    'errors': serializer.errors,
                    'data': self._get_all_data()
                }, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            
            return Response({
                'success': True,
                'message': "Data created successfully",
                'data': self._get_all_data()
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Error in POST request: {str(e)}", exc_info=True)
            return Response({
                'success': False,
                'message': f"Creation failed: {str(e)}",
                'data': self._get_all_data()
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @transaction.atomic
    def patch(self, request, *args, **kwargs):
        try:
            # Get instances that might exist
            instances = {
                key: self.get_queryset()[key].select_for_update().first()
                for key in request.data.keys()
            }

            serializer = self.get_serializer(
                instances,
                data=request.data,
                partial=True,
                context={'request': request}
            )

            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': "Validation failed",
                    'errors': serializer.errors,
                    'data': self._get_all_data()
                }, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            
            return Response({
                'success': True,
                'message': "Data updated successfully",
                'data': self._get_all_data()
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'message': f"Update failed: {str(e)}",
                'data': self._get_all_data()
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)