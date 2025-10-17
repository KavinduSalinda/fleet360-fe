from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Document
from .serializers import UserSerializer, LoginSerializer, PasswordChangeSerializer, DocumentSerializer
from .authentication import generate_jwt_token
import hashlib
from django.core.files.base import ContentFile
from django.conf import settings
import time
import os


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
        file = request.FILES.get('file')
        if not file:
            return Response({
                'message': 'File is required',
                'status': 'error',
                'code': 400
            }, status=status.HTTP_400_BAD_REQUEST)
        
        file_name = file.name
        file_hash = hashlib.sha256(file.read()).hexdigest()

        # save the file to the media directory
        # Convert file name + user id + current time to hash for a unique file name
        file_hash = hashlib.md5(
            f"{file_name}{request.user.id}{time.time()}".encode()
        ).hexdigest()
        file_hash = f"{file_hash}.pdf"

        # Define the upload path
        upload_path = os.path.join(settings.BASE_DIR, "media/documents/")

        # Ensure the upload directory exists
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)

        # Save the file in chunks to avoid memory issues with large files
        file_path = os.path.join(upload_path, file_hash)
        with open(file_path, "wb") as f:
            for chunk in file.chunks():
                f.write(chunk)

        file_url = f'{settings.MEDIA_URL}documents/{file_hash}'

        document = Document.objects.create(file_name=file_name, file_hash=file_hash, file_url=file_url, uploaded_by=request.user)
        return Response({
            'message': 'Document uploaded successfully',
            'status': 'success',
            'code': 200,
            'data': {
                'file_name': file_name,
                'file_hash': file_hash,
                'file_url': file_url
            }
        })