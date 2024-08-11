import jwt
import logging
import environ
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from bson import ObjectId
from django.utils.decorators import method_decorator
from .models import Administrator
from .serializers import AdministratorSerializer, LoginSerializer
from .authentication import is_logged_in, is_administrator , is_Admin

env = environ.Env()
SECRET_KEY = env('SECRET_KEY')



logger = logging.getLogger(__name__)


# ------------------------------------------------------------All Admin related API----------------------------------------------------------------------------------------------------

# { Admin registration by system only }
# class SuperAdminRegistration(APIView):
#     permission_classes = []

#     def post(self, request):
#         request.data['role']='Admin'
#         serializer = AdminSerializer(data=request.data)

#         if serializer.is_valid():
#             admin = serializer.save()

#             return Response({
#                 'message': 'Admin created successfully',
#                 'payload':serializer.data
#             }, status=status.HTTP_200_OK)

#         return Response({'error': 'Registration failed for admin'}, status=status.HTTP_401_UNAUTHORIZED)

from .utils import *
# {Administrator Approve by Admin only}
class ApproveAdministrator(APIView):
    @method_decorator(is_logged_in)
    @method_decorator(is_Admin)
    def post(self, request):
        administrator = Administrator.objects.get(username=request.data['Admins_username'])
        if not administrator.is_approved:
            administrator.approve()
            # send_email_to_client()
            return Response({'message': 'Administrator approved successfully.'}, status=status.HTTP_200_OK)
        return Response({'message': 'Administrator is already approved.'}, status=status.HTTP_400_BAD_REQUEST)



class getALLUnApprovedAdministrator(APIView):
    @method_decorator(is_logged_in)
    @method_decorator(is_Admin)
    def get(self, request):
        # Query all unapproved administrators
        unapproved_administrators = Administrator.objects.filter(is_approved=False)
        
        # Serialize the queryset
        serializer = AdministratorSerializer(unapproved_administrators, many=True)
        
        # Return the serialized data in the response
        return Response({'message': 'All unapproved administrators.', 'payload': serializer.data})


# -------------------------------------------------------All Administrator related api---------------------------------------------------------------------------------

# {Administrator registration}

class RegisterAdministrator(APIView):
    permission_classes = []

    def post(self, request):
        # Check if user exists
        if Administrator.objects.filter(username=request.data['username']).first():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

         # Check if email exists
        if Administrator.objects.filter(email_address=request.data['email_address']).first():
            return Response({'error': 'Email address already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        # school_license_pdf = request.FILES.get('school_license_pdf')
        request.data['role'] = 'Administrator'
        serializer = AdministratorSerializer(data=request.data)

        if serializer.is_valid():
            administrator = serializer.save()
            logger.info(f"Administrator {request.data['username']} registered.")
            return Response({
                'message': "Administrator registered successfully!",
                'payload': serializer.data,
            }, status=status.HTTP_201_CREATED)

        return Response({'error': 'Registration failed', 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# {Login based on role}
class LoginView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data
            logger.info(f"User ID: {user['id']}")

            refresh = RefreshToken.for_user(user)

            response = Response({
                'message': f'{user["role"]} logged in successfully',
                'token': str(refresh.access_token),
                'refresh_token': str(refresh),
            }, status=status.HTTP_200_OK)

            # Set the JWT token as a cookie
            response.set_cookie(
                key='jwt_token', 
                value=str(refresh.access_token), 
                httponly=True, 
                secure=False,  # Set to True in production
                samesite='Lax',
                path='/'
            )

            response.headers['Authorization'] = str(refresh.access_token)
            logger.info("Cookie set with token")

            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Random testing purpose
@is_logged_in
@is_administrator
def AppRi(request):
    return JsonResponse({
        'message': 'You are authenticated', 
        'user_id': request.user_id, 
        'administrator': request.Administrator
    })