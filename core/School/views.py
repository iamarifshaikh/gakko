# from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import School
from .serializer import SchoolSerializer
from Class.models import ClassDivision,ClassStandard
from rest_framework import status
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login

# -------------- School REgistration -----------------
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
    def delete(self, request):
        school_id = request.data.get('school_id')
        if not school_id:
            return Response({'message': 'School ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            school = School.objects.get(school_id=school_id)
            school.delete()
            return Response({'message': 'School deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response({'message': 'School not found'}, status=status.HTTP_404_NOT_FOUND)

# ------------------ school approve -------------------
class ApproveSchool(APIView):
    def post(self, request):
        try:
            # Try to retrieve the school by email
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