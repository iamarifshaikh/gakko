from rest_framework import serializers
from .models import *
from rest_framework import serializers

class AdministratorSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)  # Handle ObjectId as a string
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)
    is_approved = serializers.BooleanField(read_only=True)
    approval_date = serializers.DateTimeField(read_only=True)
    is_rejected = serializers.BooleanField(required=False)
    rejection_date = serializers.DateTimeField(read_only=True)
    school_name = serializers.CharField(required=True)
    school_address = serializers.CharField(allow_blank=True)
    contact_number = serializers.CharField(required=True)
    email_address = serializers.EmailField(required=True)
    school_type = serializers.CharField(required=True)
    approved_By = serializers.CharField(allow_blank=True, required=False)
    role = serializers.CharField()
    unique_ID = StringField()
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        administrator = Administrator(**validated_data)
        administrator.set_password(password)
        administrator.save()
        return administrator

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.is_approved = validated_data.get('is_approved', instance.is_approved)
        instance.approval_date = validated_data.get('approval_date', instance.approval_date)
        instance.is_rejected = validated_data.get('is_rejected', instance.is_rejected)
        instance.rejection_date = validated_data.get('rejection_date', instance.rejection_date)
        instance.school_name = validated_data.get('school_name', instance.school_name)
        instance.school_address = validated_data.get('school_address', instance.school_address)
        instance.contact_number = validated_data.get('contact_number', instance.contact_number)
        instance.email_address = validated_data.get('email_address', instance.email_address)
        instance.school_type = validated_data.get('school_type', instance.school_type)
        instance.approved_By = validated_data.get('approved_By', instance.approved_By)
        instance.role = validated_data.get('role',instance.role)
        instance.unique_ID = validated_data.get('unique_ID',instance.unique_ID)
        
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        
        instance.save()
        return instance

class AdminSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)  # Handle ObjectId as a string
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)
    role = serializers.CharField()



    def create(self,validated_data):
        password = validated_data.pop('password')
        admin = Superadmin(**validated_data)
        admin.set_password(password)
        admin.save()
        return admin


    def update(self,instance,validated_data):
        instance.username = validated_data.get('username',instance.username)
        instance.email = validated_data.get('email',instance.email)
        instance.role = validated_data.get('role',instance.role)
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])

        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=['Administrator', 'Teacher', 'Parent', 'Admin'])

    def validate(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        password = validated_data.get('password')
        role = validated_data.get('role')

        if role == 'Administrator':
            user = Administrator.objects.filter(username=username).first()
            if user:
                if user.is_approved == False:
                    raise serializers.ValidationError("Your account is not approved yet.")
                if user.check_password(password):
                    return user
                else:
                    raise serializers.ValidationError({"non_field_errors": ["Invalid credentials"]})
            else:
                raise serializers.ValidationError({"non_field_errors": ["User not found"]})

        elif role == 'Admin':
            correct_password = 'admin12as!@AS'
            correct_username = 'Admin123'  # Assuming you want to check this, though it's not in the form

            if username != correct_username:
                raise serializers.ValidationError("Invalid username for Admin") 

            if password != correct_password:
                raise serializers.ValidationError("Invalid password for Admin")

            user = Superadmin.objects.filter(username=username).first()
            if user:
                return user
            else:
                raise serializers.ValidationError({"non_field_errors": ["Admin account not found"]})

        else:
            raise serializers.ValidationError({"non_field_errors": ["Invalid role or credentials."]})

        return validated_data