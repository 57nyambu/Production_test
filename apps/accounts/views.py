from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated
from .serializers import CustomUserSerializer, LoginSerializer, PasswordResetSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework_simplejwt.exceptions import InvalidToken
from apps.utils.emailService import welcomeEmail
from django.shortcuts import render

#from apps.utils.email_service.send_email_service import reg_email

def home(request):
    return render(request, 'default.html') 

class RegisterUserView(APIView):
    def post(self, request):
        user_data = request.data
        serializer = CustomUserSerializer(data=user_data)
        if serializer.is_valid():
            serializer.save()

            welcomeEmail(user_data)

            user = serializer.data
            
            return Response({
                'data': user,
                'message': "Welcome to the team!",
            }, status=status.HTTP_201_CREATED)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    


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
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token", None)

            if not refresh_token:
                return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
        except InvalidToken as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetView(APIView): 
    def post(self, request): 
        serializer = PasswordResetSerializer(data=request.data, context={'request': request}) 
        if serializer.is_valid(): 
            serializer.save() 
            return Response({
                "message": "Password reset link sent."
                }, status=status.HTTP_200_OK) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': "Protected andpoint accessible to authenticated users."})