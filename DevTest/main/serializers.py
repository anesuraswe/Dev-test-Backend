from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Employee, Company, Department, Profile

# Serializer for Employee model
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee  # Specify the model for the serializer
        fields = '__all__'  # Include all fields from the model

# Serializer for Company model
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company  # Specify the model for the serializer
        fields = '__all__'  # Include all fields from the model

# Serializer for Department model
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department  # Specify the model for the serializer
        fields = '__all__'  # Include all fields from the model

# Serializer for Role model (Note: This serializer is incorrectly using Department model)
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department  # This should be Role model
        fields = '__all__'  # Include all fields from the model

# Serializer for User model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # Specify the model for the serializer
        fields = ['username', 'password', 'email']  # Specify the fields to include
        extra_kwargs = {'password': {'write_only': True}}  # Make password write-only for security

    def create(self, validated_data):
        # Create a new user with validated data
        user = User.objects.create_user(**validated_data)
        return user

# Serializer for Profile model
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile  # Specify the model for the serializer
        fields = ['first_name', 'middle_name', 'last_name', 'email', 'phone_number', 'full_name']  # Specify the fields to include
        read_only_fields = ['full_name']  # Make full_name read-only as it's a property

    def create(self, validated_data):
        # Extract user data from validated data
        user_data = validated_data.pop('user')
        # Create a new user with user data
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        # Create or update a profile with the validated data
        profile, created = Profile.objects.update_or_create(user=user, **validated_data)
        return profile
