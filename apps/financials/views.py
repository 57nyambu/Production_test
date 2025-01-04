from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import CombinedSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics
from apps.subscriptions.permissions import HasActiveSubscription


class BaseCreateAPIView(generics.CreateAPIView):
    """
    A base class for CreateAPIView that standardizes the response format
    and provides flexibility for subclasses.
    """
    success_message = "Data saved successfully."
    failure_message = "Failed to save data."

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                instance = serializer.save()
                response_data = {
                    "success": True,
                    "message": self.success_message,
                    "data": {
                        "modelId": str(instance.id),  #model identifier
                        **serializer.data,           # All saved data
                    },
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            except Exception as e:
                # unexpected sneaky MFng errors during save
                return Response(
                    {
                        "success": False,
                        "message": f"Unexpected error: {str(e)}",
                        "data": None,
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        else:
            return Response(
                {
                    "success": False,
                    "message": self.failure_message,
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
            try:
                self.perform_update(serializer)
                return Response(
                    {
                        "success": True,
                        "message": "Data updated successfully.",
                        "data": serializer.data,  # Updated data
                    },
                    status=status.HTTP_200_OK,
                )
            except Exception as e:
                return Response(
                    {
                        "success": False,
                        "message": f"An error occurred during update: {str(e)}",
                        "data": None,
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        else:
            return Response(
                {
                    "success": False,
                    "message": "Validation failed.",
                    "data": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class CombinedCreateAPIView(BaseCreateAPIView):
    permission_classes = [IsAuthenticated, HasActiveSubscription]  # Ensure only authenticated users can access
    serializer_class = CombinedSerializer

    def create(self, request, *args, **kwargs):
        # Include the logged-in user in the data
        user = request.user
        data = request.data.copy()  # Make a mutable copy of the request data

        # Inject user information into the serializer's data
        for key in self.serializer_class._declared_fields.keys():
            if isinstance(data.get(key), dict):  # Ensure it's a dict for nested serializers
                data[key]['user'] = user.id

        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            instance_mapping = serializer.save()

            response_data = {
                "success": True,
                "message": "Data saved successfully.",
                "data": {
                    "modelIds": {key: str(instance.id) for key, instance in instance_mapping.items()},
                    **serializer.data,
                },
            }

            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(
            {
                "success": False,
                "message": "Failed to save data.",
                "data": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    

class CombinedUpdateAPIView(BaseUpdateAPIView):
    """
    Handles display and update of combined model data.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CombinedSerializer

    def get(self, request, *args, **kwargs):
        """
        Fetch and display existing instance data for all models.
        """
        # Preload instances based on request or default logic
        instance_mapping = self.get_instance_mapping_for_display(kwargs)
        
        # Serialize the preloaded data
        serializer = self.get_serializer(instance_mapping)
        
        return Response(
            {
                "success": True,
                "message": "Data fetched successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def get_instance_mapping_for_display(self, kwargs):
        """
        Custom logic to fetch and return all relevant instances for display.
        """
        # Example logic: Fetch instances by IDs in kwargs or default to user's related data
        instance_mapping = {}
        for model_key in self.serializer_class._declared_fields.keys():
            model_class = self.serializer_class._declared_fields[model_key].Meta.model
            try:
                instance_mapping[model_key] = model_class.objects.filter(user=self.request.user).first()
            except model_class.DoesNotExist:
                continue
        return instance_mapping
