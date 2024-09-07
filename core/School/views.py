# from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import School
from .serializer import SchoolSerializer
from Class.models import ClassDivision,ClassStandard
from rest_framework import status
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from .utils.adminCheck import *
from django.db import transaction

# -------------- School Registration -----------------
class SchoolRegistration(APIView):
    def post(self, request):
        # Check if the school already exists
        if School.objects.filter(school_email=request.data.get('school_email')).first():
            return Response({'message': 'School already exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = SchoolSerializer(data=request.data)

        if serializer.is_valid():
            # Save the validated data and get the School instance
            school = serializer.save()

            return Response({
                'school_id': school.school_id,  # Assuming school_id is a field in the model
                'payload': serializer.data
            }, status=status.HTTP_201_CREATED)

        # Return validation errors if the data is not valid
        return Response({'error': 'Registration failed', 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# -------------- Login School  -------------------
class LoginSchool(APIView):
    def post(self, request):
        # Extract username and password from the request
        school_id = request.data.get('school_id')
        password = request.data.get('password')

        # Perform authentication
        user = authenticate(request, school_id=school_id, password=password)
        if user is not None:
            # Log the user in
            login(request, user)
            
            try:
                # Assuming the school ID is stored in the user profile
                school = School.objects.get(school_id=user.profile.school_id)  # Adjust according to your user model 
                
                if not school.classes_defined:
                    # Redirect to DefineClasses if classes are not defined
                    return redirect('define-classes')  # Adjust according to your URL patterns

                # Continue with the usual login flow
                # For example, redirect to a dashboard or homepage
                return redirect('home')  # Adjust according to your URL patterns

            except School.DoesNotExist:
                return Response({'error': 'School not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Return an error response if authentication fails
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
        
# --------------- Delete School ------------------------
class DeleteSchool(APIView):
    def delete(self, request,id):

        logger.info(f"Received delete request for School ID: {id}")
        
        try:
            school = School.objects.get(id=id)
            school.delete()
            return Response({'message': 'School deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response({'message': 'School not found'}, status=status.HTTP_404_NOT_FOUND)

# ------------------ school approve -------------------
class ApproveSchool(APIView):
    @method_decorator(admin_required)
    def post(self, request):    
        try:
            # Try to retrieve the school by id
            school = School.objects.get(id=request.data.get('id'))
            
            # Check if the school is already verified
            if not school.verified:
                 with transaction.atomic():
                    school.approve()  # Approve the school

                    # Create default classes
                    standards = [std for std in ClassStandard]
                    divisions = [div for div in ClassDivision]
                    for standard in standards:
                        for division in divisions:
                            Class.objects.create(
                                class_std=standard,
                                class_division=division,
                                school=school
                            )
                
            return Response({'message': 'School approved and classes created successfully.'}, status=status.HTTP_200_OK)
            
            return Response({'message': 'School is already approved.'}, status=status.HTTP_400_BAD_REQUEST)
        
        except School.DoesNotExist:
            return Response({'error': 'School not found'}, status=status.HTTP_404_NOT_FOUND)
            
            # If the school is already verified
            return Response({'message': 'School is already approved.'}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            # Catch any other exceptions and return a generic error message
            return Response({'error': 'An error occurred.', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ------------------- School update -----------------------------
class Updateschool(APIView):
    def patch(self,request,id):
        try:
            school = School.objects.get(id=id)
            serializer = SchoolSerializer(school, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': 'An error occurred.', 'details': str(e)}, status=status.HTTP_201_CREATED)


# ----------------- Read all School ---------------------------------

class ReadVerifiedSchool(APIView):
    def get(self,request):
        try:

            school = School.objects.filter(verified=True)

            serializer = SchoolSerializer(school,many=True)

            return Response(serializer.data,status=status.HTTP_200_OK)
            
            # return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({'error': 'An error occurred.', 'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)



# ------------------ Read unverified School ------------------------------------

class ReadUnverifiedSchool(APIView):
    def get(self,request):
        try:
            school = School.objects.filter(verified=False)

            serializer = SchoolSerializer(school,many=True)
        
            return Response(serializer.data,status=status.HTTP_200_OK)
    
        except Exception as e:
            return Response({'error': 'An error occurred.', 'details': str(e)},status=status.HTTP)