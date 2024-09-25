from rest_framework import serializers
from .models import *
from datetime import datetime, timezone

class TeacherSerializer(serializers.Serializer):
    teacher_id = serializers.CharField(read_only=True)
    teacher_name = serializers.CharField(required=True)
    teacher_email = serializers.CharField(required=True)
    teacher_number = serializers.IntegerField(required=True)
    created_at = serializers.CharField(required=False)
    updated_at = serializers.CharField(required=False)
    school_id = serializers.CharField(required=True)

    def create(self,validated_data):
        return Teacher(**validated_data).save()

    def update(self, instance, validated_data):
        instance.teacher_name = validated_data.get('teacher_name', instance.teacher_name)
        instance.teacher_email = validated_data.get('teacher_email', instance.teacher_email)
        instance.teacher_number = validated_data.get('teacher_number', instance.teacher_number)
        instance.updated_at = datetime.now(timezone.utc)
        instance.save()
        return instance

   