from django.http import JsonResponse
import jwt
from .models import *
from .serializers import *
from functools import wraps

import environ
env = environ.Env()
SECRET_KEY = env('SECRET_KEY')

def is_logged_in(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Retrieve the token from cookies
        
        token = request.headers.get('Authorization')

        if not token:
            return JsonResponse({'error': 'Token not provided'}, status=401)

        try:
            # Decode the token
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            request.user_id = decoded_token['user_id']  # Extract user ID from token

            # role = decoded_token['role']
            # request.user_role = role


        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Token has expired'}, status=401)
        except jwt.InvalidTokenError as e:
            return JsonResponse({'error': 'Invalid token', 'details': str(e)}, status=401)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

        # Call the original view function
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def is_administrator(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user_id = getattr(request, 'user_id', None)
        if user_id is None:
            return JsonResponse({'error': 'User ID not provided'}, status=400)

        try:
            user = Administrator.objects.get(id=user_id)
        except Administrator.DoesNotExist:
            return JsonResponse({'error': 'Administrator not found'}, status=404)

        if user.role != 'Administrator':
            return JsonResponse({'error': 'You are not an administrator'}, status=403)

        # Serialize the Administrator object
        serializer = AdministratorSerializer(user).data

        # Attach the serialized data to the request
        request.Administrator = serializer

        # Call the view function with the modified request
        return view_func(request, *args, **kwargs)

    return _wrapped_view



def is_Admin(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user_id = getattr(request, 'user_id', None)
        if user_id is None:
            return JsonResponse({'error': 'User ID not provided'}, status=400)

        try:
            user = Superadmin.objects.get(id=user_id)
        except Superadmin.DoesNotExist:
            return JsonResponse({'error': 'Admin not found or you are not an admin'}, status=404)

        if user.role != 'Admin':
            return JsonResponse({'error': 'You are not an Admin'}, status=403)

        # Serialize the Administrator object
        serializer = AdminSerializer(user).data

        # Attach the serialized data to the request
        request.Admin = serializer

        # Call the view function with the modified request
        return view_func(request, *args, **kwargs)

    return _wrapped_view