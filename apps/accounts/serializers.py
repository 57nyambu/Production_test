from rest_framework import serializers
from .models import CustomUser
from apps.subscriptions.models import Subscription
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode 
from django.utils.encoding import force_bytes
from apps.utils.emailService import forgotPassEmail

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'company', 'password']


    def create(self, validated_data):
        # Automatically hash passwords
        user = CustomUser.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            company=validated_data['company'],
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            self.user = CustomUser.objects.get(email=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("No user found with this email address.")
        return value

    def save(self):
        user = self.user
        # Generate token
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        # Create reset link - replace with your frontend URL
        reset_url = f"https://finarchitect.com/reset-password/{uid}/{token}/"
        
        # Send email
        forgotPassEmail(user, reset_url)
        return True


class PasswordResetConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8, write_only=True)
    token = serializers.CharField()
    uidb64 = serializers.CharField()

    def validate(self, data):
        try:
            uid = urlsafe_base64_decode(data['uidb64']).decode()
            self.user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, CustomUser.DoesNotExist):
            raise serializers.ValidationError("Invalid reset link")

        if not default_token_generator.check_token(self.user, data['token']):
            raise serializers.ValidationError("Invalid or expired token")

        return data

    def save(self):
        self.user.set_password(self.validated_data['password'])
        self.user.save()
        return self.user 

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'first_name', 
            'last_name',
            'email',  
            'company',
            'password',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def update(self, instance, validated_data):
        # Update user fields
        for attr, value in validated_data.items():
            if attr == 'password':  # Handle password separately
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


class AdminUserSubscriptionSerializer(serializers.ModelSerializer):
    plan_name = serializers.CharField(source='plan.name')
    plan_price = serializers.DecimalField(source='plan.price', max_digits=10, decimal_places=2)
    
    class Meta:
        model = Subscription
        fields = ['plan_name', 'plan_price', 'is_active', 'start_date', 'end_date']

class AdminUserDetailSerializer(serializers.ModelSerializer):
    subscription = AdminUserSubscriptionSerializer(read_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'company', 'date_joined', 'last_login', 'is_active', 'subscription']
