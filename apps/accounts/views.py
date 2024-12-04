from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import CustomUserSerializer, LoginSerializer, PasswordResetSerializer, LogoutSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

#from apps.utils.email_service.send_email_service import reg_email

class RegisterUserView(APIView):
    def post(self, request):
        user_data = request.data
        serializer = CustomUserSerializer(data=user_data)
        if serializer.is_valid():
            serializer.save()

            user = serializer.data
            
            return Response({
                'data': user,
                'message': "Welcome to the team!",
            }, status=status.HTTP_201_CREATED)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(f"{user_data['email']} is already registered!", status=status.HTTP_400_BAD_REQUEST)
    


class LoginView(APIView):
    permission_classes=[permissions.AllowAny]
    serializer_class = LoginSerializer  # Reference the class properly

    def post(self, request):
        user_data = request.data
        # Use self.serializer_class to correctly refer to the serializer class
        serializer = self.serializer_class(data=user_data)

        if serializer.is_valid():
            # Extract validated data
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')

            user = authenticate(request, email=email, password=password)
            if user:
                # Generate tokens using the authenticated user
                refresh = RefreshToken.for_user(user)
                return Response({
                    'message': 'Login successful',
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                }, status=status.HTTP_200_OK)

            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            # Extract the refresh token from the request
            refresh_token = serializer.validated_data.get('refresh_token')
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()  # This will only work if blacklisting is enabled
                return Response({"message": "Logout successful"}, status=status.HTTP_204_NO_CONTENT)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

class PasswordResetView(APIView): 
    def post(self, request): 
        serializer = PasswordResetSerializer(data=request.data, context={'request': request}) 
        if serializer.is_valid(): 
            serializer.save() 
            return Response({
                "message": "Password reset link sent."
                }, status=status.HTTP_200_OK) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminView(APIView):
    permission_classes=[permissions.IsAdminUser]

    def get(self, request):
        return Response({'message': 'Admin Authentication working'}
                        , status=status.HTTP_200_OK)
    

class RegularUserView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def get(self, request):
        return Response({'message': 'User Authentication working'}
                        , status=status.HTTP_200_OK)