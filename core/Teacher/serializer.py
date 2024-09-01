from rest_framework import serializers
from .models import *
from datetime import datetime
from django.utils import timezone 

class TeacherSerializer(serializers.Serializer):
    teacher_id = serializers.CharField(read_only=True)
    teacher_name = serializers.CharField(required=True)
    teacher_email = serializers.CharField(required=True)
    teacher_number = serializers.IntegerField(required=True)
    created_at = serializers.CharField(required=False)
    updated_at = serializers.CharField(required=False)
    school_id = serializers.CharField(required=True)

    def create(self,validated_data):
        return School.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.teacher_name = validated_data.get('teacher_name', instance.teacher_name)
        instance.teacher_email = validated_data.get('teacher_email', instance.teacher_email)
        instance.teacher_number = validated_data.get('teacher_number', instance.teacher_number)
        instance.updated_at = datetime.now(timezone.now)
        instance.save()
        return instance

   