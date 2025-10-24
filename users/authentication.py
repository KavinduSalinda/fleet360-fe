import jwt
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework import authentication, exceptions
from django.contrib.auth import get_user_model

User = get_user_model()

# users/authentication.py
class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # Skip authentication for login endpoint
        if request.path.endswith('/login/') and request.method == 'POST':
            return None
            
        token = self.get_token_from_request(request)
        if not token:
            return None
        
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            user_id = payload.get('id')
            if not user_id:
                return None
            
            user = User.objects.get(id=user_id)
            return (user, token)
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Invalid token')
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('User not found')
    
    def get_token_from_request(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if auth_header and auth_header.startswith('Bearer '):
            return auth_header.split(' ')[1]
        return None


def generate_jwt_token(user):
    payload = {
        'id': user.id,
        'email': user.email,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(seconds=settings.JWT_ACCESS_TOKEN_LIFETIME)
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
