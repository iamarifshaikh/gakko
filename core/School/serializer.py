from rest_framework import serializers
from .models import *

class SchoolSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    school_id = serializers.CharField(required=False)
    school_name = serializers.CharField(required=True)
    school_email = serializers.CharField(required=True)
    school_number = serializers.IntegerField(required=True)
    created_at = serializers.CharField(required=False)
    approved_at = serializers.CharField(allow_blank=True, required=False)
    verified = serializers.BooleanField(default=False)
    school_license = serializers.FileField(required=False)
    password = serializers.CharField(required=False, write_only=True)
    principal_name = serializers.CharField(required=True)

    def create(self,validated_data):
        return School.objects.create(**validated_data)
        

    def update(self,instance,validated_data):
        password = validated_data.pop('password',None)
        if password:
            instance.set_password(password)
        
        if 'school_id' in validated_data:
            instance.school_id = validated_data.pop('school_id')
        
        instance.school_name = validated_data.get('school_name', instance.school_name)
        instance.school_email = validated_data.get('school_name',instance.school_email)
        instance.school_number = validated_data.get('school_number',instance.school_number)
        instance.created_at = validated_data.get('created_at',instance.created_at)
        instance.approved_at = validated_data.get('approved_at',instance.approved_at)
        instance.verified = validated_data.get('verified',instance.verified)
        instance.school_license = validated_data.get('school_license',instance.school_license)
        instance.principal_name = validated_data.get('principal_name',instance.principal_name)

        instance.save()
        return instance
