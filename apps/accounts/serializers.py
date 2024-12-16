from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode 
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
            user = CustomUser.objects.get(email=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Email not found.")
        return value
    
    def save(self): 
        request = self.context.get('request') 
        user = CustomUser.objects.get(email=self.validated_data['email'])
        token = default_token_generator.make_token(user) 
        uid = urlsafe_base64_encode(force_bytes(user.pk)) 
        reset_link = request.build_absolute_uri(f'/reset-password/{uid}/{token}/') 
        email = user.email
        #send_mail( 
        #    'Password Reset Request', 
        #    f'Click the link to reset your password: {reset_link}', 
        #    'from@example.com', [user.email], fail_silently=False, )
        forgotPassEmail(user, reset_link)

        return email
    

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
