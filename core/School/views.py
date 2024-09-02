# from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import School
from .serializer import SchoolSerializer
from rest_framework import status
from django.utils.decorators import method_decorator
from .utils.adminCheck import *

#------- School Registration -----------------
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


# --------------- Delete School ------------------------

class DeleteSchool(APIView):
    def delete(self, request,id):
        
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
                school.approve()  # Approve the school
                return Response({'message': 'School approved successfully.'}, status=status.HTTP_200_OK)
            
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