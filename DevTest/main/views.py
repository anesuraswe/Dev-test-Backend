from rest_framework import viewsets
from .models import Employee, Company, Department, Role, Profile
from django.shortcuts import render, redirect
from .serializers import EmployeeSerializer, CompanySerializer, DepartmentSerializer, RoleSerializer,  UserSerializer, ProfileSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
import json
import csv
from io import StringIO

# Define viewsets for each model to handle CRUD operations
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

# Function to handle user signup
@csrf_exempt
@api_view(['POST'])
def signup(request):
    # Extract user and profile data from request
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

    # Validate and save user data
    user_serializer = UserSerializer(data=user_data)
    if user_serializer.is_valid():
        user = user_serializer.save()
        # Associate user with profile data and save
        profile_data['user'] = user
        profile_serializer = ProfileSerializer(data=profile_data)
        if profile_serializer.is_valid():
            profile_serializer.save()
            # Generate token for the user
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': user_serializer.data,
                'profile': profile_serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Function to handle user signin
@csrf_exempt
@api_view(['POST'])
def signin(request):
    # Extract credentials from request
    username = request.data.get('username')
    password = request.data.get('password')
    # Authenticate user
    user = authenticate(username=username, password=password)
    if user:
        # Generate token for the user
        token, created = Token.objects.get_or_create(user=user)
        try:
            # Retrieve user's profile
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

# Function to retrieve all data
@csrf_exempt
@api_view(['GET'])
def get_all_data(request):
    try:
        # Retrieve all data from models
        employees = Employee.objects.all()
        companies = Company.objects.all()
        departments = Department.objects.all()
        roles = Role.objects.all()
        profiles = Profile.objects.all()

        # Serialize the data
        employee_serializer = EmployeeSerializer(employees, many=True)
        company_serializer = CompanySerializer(companies, many=True)
        department_serializer = DepartmentSerializer(departments, many=True)
        role_serializer = RoleSerializer(roles, many=True)
        profile_serializer = ProfileSerializer(profiles, many=True)

        return Response({
            'employees': employee_serializer.data,
            'companies': company_serializer.data,
            'departments': department_serializer.data,
            'roles': role_serializer.data,
            'profiles': profile_serializer.data
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Function to handle CSV file upload
@csrf_exempt
@api_view(['POST'])
@parser_classes([MultiPartParser])
def upload_csv(request):
    if 'file' not in request.FILES:
        return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    file = request.FILES['file']
    decoded_file = file.read().decode('utf-8')
    io_string = StringIO(decoded_file)
    csv_reader = csv.reader(io_string, delimiter=',')

    header = next(csv_reader)
    
    for row in csv_reader:
        # Process CSV data based on the number of fields
        if len(row) == 8:  # Assuming the CSV for companies has 8 fields
            name, registration_date, registration_number, address, contact_person, number_of_employees, contact_phone, email = row

            company_data = {
                'name': name,
                'registration_date': registration_date,
                'registration_number': registration_number,
                'address': address,
                'contact_person': contact_person,
                'number_of_employees': number_of_employees,
                'contact_phone': contact_phone,
                'email': email
            }
            company_serializer = CompanySerializer(data=company_data)
            if company_serializer.is_valid():
                company_serializer.save()
            else:
                return Response(company_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif len(row) == 10:  # Assuming the CSV for employees has 10 fields
            company_name, name, employee_id, department_name, role_name, date_started, date_left, duties = row

            # Check if company exists, if not create it
            company, created = Company.objects.get_or_create(name=company_name)
            # Check if department exists, if not create it
            department, created = Department.objects.get_or_create(name=department_name, company=company)
            # Check if role exists, if not create it
            role, created = Role.objects.get_or_create(name=role_name)

            employee_data = {
                'company': company.id,
                'name': name,
                'employee_id': employee_id,
                'department': department.id,
                'role': role.id,
                'date_started': date_started,
                'date_left': date_left,
                'duties': duties
                
            }
            employee_serializer = EmployeeSerializer(data=employee_data)
            if employee_serializer.is_valid():
                employee_serializer.save()
            else:
                return Response(employee_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif len(row) == 2:  # Assuming the CSV for roles has 2 fields
            role_name = row[0]
            role_description = row[1]

            role_data = {
                'name': role_name,
                'description': role_description
            }
            role_serializer = RoleSerializer(data=role_data)
            if role_serializer.is_valid():
                role_serializer.save()
            else:
                return Response(role_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif len(row) == 3:  # Assuming the CSV for departments has 3 fields
            company_name, department_name, department_description = row

            company, created = Company.objects.get_or_create(name=company_name)
            department_data = {
                'company': company.id,
                'name': department_name,
                'description': department_description
            }
            department_serializer = DepartmentSerializer(data=department_data)
            if department_serializer.is_valid():
                department_serializer.save()
            else:
                return Response(department_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Invalid CSV format'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': 'CSV data has been successfully uploaded and processed.'}, status=status.HTTP_200_OK)
