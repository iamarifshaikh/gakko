from functools import wraps
from django.http import JsonResponse
import environ
env = environ.Env()

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        admin_email = request.headers.get('adminmEmail')
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