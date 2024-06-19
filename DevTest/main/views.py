from rest_framework import viewsets
from .models import Employee, Company, Department, Role
from django.shortcuts import render, redirect
from .serializers import EmployeeSerializer, CompanySerializer, DepartmentSerializer, RoleSerializer
from django.views.decorators.csrf import csrf_exempt
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