from rest_framework.views import APIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework import status, permissions, viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    CustomUserSerializer, 
    LoginSerializer, 
    PasswordResetSerializer, 
    AdminUserDetailSerializer,
    PasswordResetConfirmSerializer,
    UserDetailSerializer)
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework_simplejwt.exceptions import InvalidToken
from apps.utils.emailService import welcomeEmail
from django.views.generic.base import TemplateView
import logging
from .models import CustomUser
from apps.utils.emailService import forgotPassEmail

logger = logging.getLogger(__name__)


class WelcomeView(TemplateView):
    template_name = "default.html"

class RegisterUserView(APIView): 
    def post(self, request): 
        logger.debug(f"Request Data: {request.body}") # Log incoming data 
        user_data = request.data 
        logger.debug(f"Request Data: {user_data}") # Log parsed request data 
        
        serializer = CustomUserSerializer(data=user_data) 
        if serializer.is_valid(): 
            serializer.save() 
            welcomeEmail(user_data) 
            user = serializer.data 
            response = Response({ 
                'success': True,
                'message': "User created!", 
                }, status=status.HTTP_201_CREATED) 
            response['Content-Type'] = 'application/json' 
            return response 
        response = Response({'success': False, "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST) 
        response['Content-Type'] = 'application/json' 
        return response

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
                    'success': True,
                    'message': 'Login successful',
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                }, status=status.HTTP_200_OK)

            return Response({'success': False, 'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

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

            return Response({
                "message": "Successfully logged out."}, status=status.HTTP_200_OK)
        except InvalidToken as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        try:
            if serializer.is_valid():
                data = serializer.save()
                forgotPassEmail(data)
                return Response({
                    'success': True,
                    'data': {
                        'token': data['token'],
                        'uid': data['uid'],
                        'email': data['email'],
                    }
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'success': False,
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(APIView):
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        try:
            if serializer.is_valid():
                data = serializer.save()
                return Response({
                    'success': True,
                    'data': data
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
            
        return Response({
            'success': False,
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    

class UpdateUserView(APIView):

    permission_classes = [permissions.IsAuthenticated]  # Ensure that only authenticated users can access this view

    def get(self, request):
        user = request.user  # Get the currently authenticated user
        serializer = CustomUserSerializer(user)
        # Exclude the 'id' from the response
        data = serializer.data
        data.pop('id', None)
        return Response({
            "success": True,
            "message": "User data retrieved successfully.",
            "data": data
        }, status=status.HTTP_200_OK)

    def patch(self, request):
        """
        Update current user data.
        """
        user = request.user  # Get the currently authenticated user
        serializer = CustomUserSerializer(user, data=request.data, partial=True)  # Allow partial updates

        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "User data updated successfully.",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            "success": False,
            "message": "Failed to update user data.",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class TestProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': "Protected andpoint accessible to authenticated users."})


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff or request.user.is_admin

class AdminUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all().select_related('subscription', 'subscription__plan')
    serializer_class = AdminUserDetailSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['email', 'first_name', 'last_name']
    ordering_fields = ['date_joined', 'email', 'subscription__plan__name']


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserDetailSerializer
    def get(self, request):
        try:
            serializer = self.serializer_class(request.user)
            return Response({'success': True, 'data': serializer.data
                    }, status=status.HTTP_200_OK)
        except: return Response({'success': False, 'error': 'User not found'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)