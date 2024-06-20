from rest_framework import viewsets
from .models import Employee, Company, Department, Role, Profile
from django.shortcuts import render, redirect
from .serializers import EmployeeSerializer, CompanySerializer, DepartmentSerializer, RoleSerializer,  UserSerializer, ProfileSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
import json

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

@csrf_exempt
@api_view(['POST'])
def signup(request):
    user_data = {
        'username': request.data.get('username'),
        'password': request.data.get('password'),
        'email': request.data.get('email')
    }
    profile_data = {
        'first_name': request.data.get('first_name'),
        'middle_name': request.data.get('middle_name'),
        'last_name': request.data.get('last_name'),
        'email': request.data.get('email'),
        'phone_number': request.data.get('phone_number')
    }

    user_serializer = UserSerializer(data=user_data)
    if user_serializer.is_valid():
        user = user_serializer.save()
        profile_data['user'] = user
        profile_serializer = ProfileSerializer(data=profile_data)
        if profile_serializer.is_valid():
            profile_serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': user_serializer.data,
                'profile': profile_serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])
def signin(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, created = Token.objects.get_or_create(user=user)
        try:
            profile = Profile.objects.get(user=user)
            profile_serializer = ProfileSerializer(profile)
            return Response({
                'token': token.key,
                'user': UserSerializer(user).data,
                'profile': profile_serializer.data
            }, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({'error': 'Profile not found for the user'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)
