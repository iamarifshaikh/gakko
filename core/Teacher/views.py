# from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Teacher
from .serializer import TeacherSerializer
from rest_framework import status
from TeacherRoles.serializers import TeacherRoleSerializer, Roles

#------- Add a Teacher -----------------
class AddTeacher(APIView):
    def post(self, request):
        # Check if the teacher already exists
        if Teacher.objects.filter(teacher_email=request.data.get('teacher_email')).first():
            return Response({'message': 'Teacher with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TeacherSerializer(data=request.data)

        if serializer.is_valid():
            teacher = serializer.save()

            if(request.data.get('role_type') == 'class' and request.data.get('class_id')):
                data = {
                    "teacher_id": teacher.teacher_id,
                    "role_type": Roles.classTeacher,
                    "class_id": request.data.get('class_id'),
                    "school_id": request.data.get('school_id')
                }
                roleSerializer = TeacherRoleSerializer(data=data)

                if roleSerializer.is_valid():
                    roleSerializer.save()

            return Response(TeacherSerializer(teacher).data, status=status.HTTP_201_CREATED)

        # Return validation errors if the data is not valid
        return Response({'error': 'Cannot add this teacher', 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# --------------- Read one Teacher ------------------------
class ReadOneTeacher(APIView):
    def get(self, request):
        teacher_id = request.data.get('teacher_id')
        if not teacher_id:
            return Response({'message': 'Teacher ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            teacher = Teacher.objects.get(teacher_id=teacher_id)
            return Response(TeacherSerializer(teacher).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'Teacher not found'}, status=status.HTTP_404_NOT_FOUND)

# --------------- Read All Teacher ------------------------
class ReadAllTeacher(APIView):
    def get(self, request):
        school_id = request.data.get('school_id')
        if not school_id:
            return Response({'message': 'School ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            teachers = Teacher.objects.get(school_id=school_id)
            return Response(TeacherRoleSerializer(teachers).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'Teachers not found'}, status=status.HTTP_404_NOT_FOUND)

# --------------- Update Teacher ------------------------
class UpdateTeacher(APIView):
    def put(self, request, *args, **kwargs):
        try:
            teacher = Teacher.objects.get(teacher_id = request.data.get('teacher_id'))
        except Teacher.DoesNotExist:
            return Response({"error": "Teacher not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TeacherSerializer(teacher, data=request.data, partial=True) 
        
        if serializer.is_valid():
            updated_teacher = serializer.save()
            return Response(TeacherSerializer(updated_teacher).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# --------------- Delete Teacher ------------------------

class DeleteTeacher(APIView):
    def delete(self, request):
        teacher_id = request.data.get('teacher_id')
        if not teacher_id:
            return Response({'message': 'Teacher ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            teacher = Teacher.objects.get(teacher_id=teacher_id)
            teacher.delete()
            return Response({'message': 'Teacher deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response({'message': 'Teacher not found'}, status=status.HTTP_404_NOT_FOUND)
