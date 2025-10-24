from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()
from django.contrib.auth import authenticate
from .models import Document
from .authentication import generate_jwt_token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number']
    
    def update(self, instance, validated_data):
        # Update user fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        return instance


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            try:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    attrs['user'] = user
                    return attrs
                else:
                    raise serializers.ValidationError('Invalid credentials')
            except User.DoesNotExist:
                raise serializers.ValidationError('Invalid credentials')
        else:
            raise serializers.ValidationError('Must include email and password')


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("New passwords don't match")
        return attrs


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['file_name', 'file_hash', 'file_url']
