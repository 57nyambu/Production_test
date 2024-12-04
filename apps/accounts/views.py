from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import CustomUserSerializer, LoginSerializer, PasswordResetSerializer, LogoutSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
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
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Logout successful"}, status=status.HTTP_204_NO_CONTENT)
    

class PasswordResetAPIView(APIView):
    permission_classes = [permissions.AllowAny]  # Anyone can access this endpoint

    def post(self, request):
        # Step 1: Validate the email
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get['email']

            # Step 2: Find the user based on email
            try:
                user = CustomUser().objects.get(email=email)
            except CustomUser().DoesNotExist:
                return Response({"detail": "Email not found."}, status=status.HTTP_400_BAD_REQUEST)

            # Step 3: Generate token and uid
            uidb64 = urlsafe_base64_encode(str(user.pk).encode())
            token = default_token_generator.make_token(user)

            # Step 4: Prepare the reset URL
            reset_url = f"{settings.FRONTEND_URL}/reset-password/{uidb64}/{token}/"

            # Step 5: Prepare the email content
            email_subject = "Password Reset Request"
            email_body = render_to_string(
                'emails/password_reset_email.html',  # Path to your email template
                {'reset_url': reset_url, 'user': user}
            )

            # Step 6: Send email via Resend
            try:
                resend.emails.send(
                    from_email="no-reply@yourdomain.com",
                    to=[email],
                    subject=email_subject,
                    text=email_body
                )
                return Response({"detail": "Password reset email sent."}, status=status.HTTP_200_OK)
            except resend.exceptions.ResendError:
                return Response({"detail": "Failed to send email."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
