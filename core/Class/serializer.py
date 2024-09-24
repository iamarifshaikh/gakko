# from rest_framework import serializers
# # from ..School.models import Class, School
# from .models import *

# class ClassSerializer(serializers.ModelSerializer):
#     class_std = serializers.ChoiceField(choices=ClassStandard)
#     class_division = serializers.ChoiceField()
    
#     class Meta:
#         model = Class
#         fields = ['class_id', 'class_std', 'class_division', 'school_id', 'updated_at']

# class SchoolSerializer(serializers.ModelSerializer):
#     class Meta: 
#         model = School
#         fields = ['school_id', 'school_name', 'classes_defined']  # Add other fields as needed

from rest_framework import serializers
from .models import * 
from School.models import School

class ClassSerializer(serializers.Serializer):
    class_std = serializers.ChoiceField(choices=[
        (ClassStandard.NURSERY, 'Nursery'),
        (ClassStandard.JR_KG, 'Junior KG'),
        (ClassStandard.SR_KG, 'Senior KG'),
        (ClassStandard.FIRST, 'First'),
        (ClassStandard.SECOND, 'Second'),
        (ClassStandard.THIRD, 'Third'),
        (ClassStandard.FOURTH, 'Fourth'),
        (ClassStandard.FIFTH, 'Fifth'),
        (ClassStandard.SIXTH, 'Sixth'),
        (ClassStandard.SEVENTH, 'Seventh'),
        (ClassStandard.EIGHTH, 'Eighth'),
        (ClassStandard.NINTH, 'Ninth'),
        (ClassStandard.TENTH, 'Tenth')
    ])
    class_division = serializers.ChoiceField(choices=[
        (ClassDivision.A, 'A'),
        (ClassDivision.B, 'B'),
        (ClassDivision.C, 'C'),
        (ClassDivision.D, 'D'),
        (ClassDivision.E, 'E')
    ])

    class Meta:
        model = Class
        fields = ['class_std', 'class_division', 'school_id', 'updated_at']


class SchoolSerializer(serializers.Serializer):
    class Meta:
        model = School
        fields = ['school_id', 'school_name', 'classes_defined']
