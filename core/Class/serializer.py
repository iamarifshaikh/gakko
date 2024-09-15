from rest_framework import serializers
from ..School.models import Class, School

class ClassSerializer(serializers.ModelSerializer):
    class_std = serializers.ChoiceField(choices=ClassStandard.choices)
    class_division = serializers.ChoiceField(choices=ClassDivision.choices)
    
    class Meta:
        model = Class
        fields = ['class_id', 'class_std', 'class_division', 'school_id', 'updated_at']

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['school_id', 'school_name', 'classes_defined']  # Add other fields as needed
