import hashlib
import os
import time

from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from fleet360.responses import StandardResponse
from .authentication import generate_jwt_token
from .models import Document
from .serializers import UserSerializer, LoginSerializer, PasswordChangeSerializer, DocumentSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    
    def list(self, request, *args, **kwargs):
        raise MethodNotAllowed('LIST', detail="Listing all users is not allowed.")

    def create(self, request, *args, **kwargs):
        raise MethodNotAllowed('CREATE', detail="Creating users via this endpoint is not allowed.")

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed('PARTIAL_UPDATE', detail="Partial updates are not allowed. Use full update instead.")

    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed('DELETE', detail="Deleting users via this endpoint is not allowed.")
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        token = generate_jwt_token(user)

        data = {
                'access_token': token,
                'user': UserSerializer(user).data
            }
        
        return StandardResponse(
            data=data,
            message="User retrieved successfully",
            code=status.HTTP_200_OK,
        )
    
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']
        
        if not user.check_password(old_password):
            return StandardResponse(
                message="Invalid old password",
                code=status.HTTP_400_BAD_REQUEST,
            )
        
        user.set_password(new_password)
        user.save()

        return StandardResponse(
            message="Password changed successfully",
            code=status.HTTP_200_OK,
        )


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Document.objects.filter(uploaded_by=self.request.user)

    def list(self, request, *args, **kwargs):
        raise MethodNotAllowed('LIST', detail="Listing all documents is not allowed.")

    def retrieve(self, request, *args, **kwargs):
        raise MethodNotAllowed('CREATE', detail="Creating documents via this endpoint is not allowed.")

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed('PARTIAL_UPDATE', detail="Partial updates are not allowed.")

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed('UPDATE', detail="Updating documents is not allowed.")

    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed('DELETE', detail="Deleting users via this endpoint is not allowed.")
    
    def create(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if not file:
            return StandardResponse(
                message='File is required',
                code=status.HTTP_400_BAD_REQUEST
            )
        
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
        data = {
            'file_name': file_name,
            'file_hash': file_hash,
            'file_url': file_url
        }

        return StandardResponse(
            message="Document uploaded successfully",
            code=status.HTTP_201_CREATED,
            data=data
        )