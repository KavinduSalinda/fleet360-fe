from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Document
from .serializers import UserSerializer, LoginSerializer, PasswordChangeSerializer, DocumentSerializer
from .authentication import generate_jwt_token


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def list(self, request, *args, **kwargs):
        # Return current user's details
        serializer = self.get_serializer(request.user)
        return Response({
            'data': serializer.data,
            'message': 'Data received successfully',
            'status': 'success',
            'code': 200
        })
    
    def retrieve(self, request, *args, **kwargs):
        # Return current user's details
        serializer = self.get_serializer(request.user)
        return Response({
            'data': serializer.data,
            'message': 'Data received successfully',
            'status': 'success',
            'code': 200
        })
    
    def update(self, request, *args, **kwargs):
        # Update current user's details
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            'data': serializer.data,
            'message': 'User updated successfully',
            'status': 'success',
            'code': 200
        })
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        token = generate_jwt_token(user)
        
        return Response({
            'data': {
                'access_token': token,
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                }
            },
            'message': 'User retrieved successfully',
            'status': 'success',
            'code': 200
        })
    
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']
        
        if not user.check_password(old_password):
            return Response({
                'message': 'Old password is incorrect',
                'status': 'error',
                'code': 400
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()
        
        return Response({
            'message': 'Password changed successfully',
            'status': 'success',
            'code': 200
        })


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Document.objects.filter(uploaded_by=self.request.user)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(uploaded_by=request.user)
        
        return Response({
            'data': serializer.data,
            'message': 'Document Uploaded successfully',
            'status': 'success',
            'code': 200
        })
