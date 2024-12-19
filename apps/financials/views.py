from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import CombinedSerializer

class BaseCreateAPIView(generics.CreateAPIView):
    """
    A base class for CreateAPIView that standardizes the response format.
    """
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Data saved successfully.",
                    "data": {
                        "modelId": str(instance.id),  # Unique model identifier
                        **serializer.data,           # All saved data
                    },
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {
                    "success": False,
                    "message": "Failed to save data.",
                    "data": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class BaseUpdateAPIView(generics.UpdateAPIView):
    """
    A base class for UpdateAPIView that standardizes the response format.
    """
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(
                {
                    "success": True,
                    "message": "Data updated successfully.",
                    "data": serializer.data,  # Updated data
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "success": False,
                    "message": "Failed to update data.",
                    "data": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class CombinedCreateAPIView(BaseCreateAPIView):
    """
    A view for creating data using the CombinedSerializer.
    """
    serializer_class = CombinedSerializer

    def create(self, request, *args, **kwargs):
        # Get the serializer with the request data
        serializer = self.get_serializer(data=request.data)
        
        # Check if the serializer is valid
        if serializer.is_valid():
            # Save the validated data and create instances
            instance = serializer.save()
            
            # Prepare the success response
            return Response(
                {
                    "success": True,
                    "message": "Data saved successfully.",
                    "data": {
                        "modelId": str(instance.get('id', '')),  # Assuming 'id' is the identifier in the data returned
                        **serializer.data,                      # All saved data
                    },
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            # If the serializer is invalid, return errors
            return Response(
                {
                    "success": False,
                    "message": "Failed to save data.",
                    "data": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )