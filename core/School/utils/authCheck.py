from functools import wraps
from django.http import JsonResponse
import environ
env = environ.Env()
from ..serializer import *
import jwt

def is_admin(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        admin_email = request.headers.get('adminEmail')
        admin_password = request.headers.get('adminPassword')

        expected_admin_email = env('admin_email')
        expected_admin_password = env('admin_password')

        print(admin_email)
        print(expected_admin_email)
        # Validate the admin credentials
        if admin_email != expected_admin_email or admin_password != expected_admin_password:
            return JsonResponse({'error': 'Unauthorized. Invalid admin credentials.'}, status=401)

        # Proceed with the original view if admin credentials are valid
        return view_func(request, *args, **kwargs)

    return _wrapped_view

def is_school_logged_in(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):

        token = request.headers.get('Authorization')

        if not token:
            return JsonResponse({'error': 'Unauthorized. No token provided.'}, status=401)

        try:
            decode_token = jwt.decode(token, env('SECRET_KEY'), algorithms=['HS256'])
            print(f"Decoded token ${decode_token}")

            school = School.objects.get(id=decode_token['user_id'])
            request.school = school

        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Unauthorized. Token has expired.'}, status=401)

        except jwt.InvalidTokenError:
            return JsonResponse({'error': 'Unauthorized. Invalid token.'}, status=401)
            
        except School.DoesNotExist:
            return JsonResponse({'error': 'School not found.'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=401)
            
        return view_func(request, *args, **kwargs)
    return _wrapped_view