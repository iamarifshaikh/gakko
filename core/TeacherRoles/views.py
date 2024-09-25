# from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import TeacherRoles
from rest_framework import status
from .serializers import TeacherRoleSerializer

#------- Add a Teacher -----------------
class AddSubjectRole(APIView):
    def post(self, request):
        # Check if the subject with class_id already exists
        if TeacherRoles.objects.filter(class_id=request.data.get('class_id'), subject_name = request.data.get('subject_name')).first():
            return Response({'message': 'Teacher for the class with the same subject exist. Please do update'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TeacherRoleSerializer(data=request.data)

        if serializer.is_valid():
            teacherRole = serializer.save()
            teacherRole.role_id = str(TeacherRoles.objects.get(teacher_id=request.data.get('teacher_id'), class_id=request.data.get('class_id'),subject_name=request.data.get('subject_name')).id)
            teacherRole.save()

            return Response(TeacherRoleSerializer(teacherRole).data, status=status.HTTP_201_CREATED)

        # Return validation errors if the data is not valid
        return Response({'error': 'Cannot add this teacher role', 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# --------------- Read one Teacher ------------------------
class ReadRole(APIView):
     def get(self, request, *args, **kwargs):
        # Get query parameters from the request
        query_params = request.query_params
        
        # Build the filter criteria dynamically
        filters = {}
        for param in query_params:
            if param in ['role_type', 'school_id', 'subject_name', 'class_id',]:
                filters[param] = query_params.get(param)
        
        # Apply filters to the query
        queryset = TeacherRoles.objects.filter(**filters)
        
        # Serialize the filtered queryset
        serializer = TeacherRoleSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# --------------- Update Teacher ------------------------
class UpdateRole(APIView):
    def put(self, request, *args, **kwargs):
        try:
            teacherRole = TeacherRoles.objects.get(role_id = request.data.get('role_id'))
        except TeacherRoles.DoesNotExist:
            return Response({"error": "Teacher role not found"}, status=status.HTTP_404_NOT_FOUND)
               
        serializer = TeacherRoleSerializer(teacherRole, data=request.data,partial=True) 
        
        if serializer.is_valid():
            updated_teacher = serializer.save()
            return Response(TeacherRoleSerializer(updated_teacher).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

