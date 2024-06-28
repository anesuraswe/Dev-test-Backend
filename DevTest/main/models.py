from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# Profile model to store user's personal information
class Profile(models.Model):
    # One-to-one relationship with User model
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # First name of the user
    first_name = models.CharField(max_length=100, blank=False)
    # Middle name of the user (optional)
    middle_name = models.CharField(max_length=100, blank=True)
    # Last name of the user
    last_name = models.CharField(max_length=100, blank=False)
    # Email address of the user
    email = models.EmailField(max_length=1000, blank=False)
    # Phone number of the user
    phone_number = models.CharField(max_length=20)

    # Property to return the full name of the user
    @property
    def full_name(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}"

# Company model to store company information
class Company(models.Model):
    # Name of the company
    name = models.CharField(max_length=255)
    # Date of company registration
    registration_date = models.DateField()
    # Registration number of the company
    registration_number = models.CharField(max_length=50)
    # Address of the company
    address = models.TextField()
    # Contact person's name
    contact_person = models.CharField(max_length=255)
    # Number of employees in the company
    number_of_employees = models.IntegerField()
    # Contact phone number of the company
    contact_phone = models.CharField(max_length=15)
    # Email address of the company
    email = models.EmailField()

    # Method to return the string representation of the company
    def __str__(self):
        return self.name

# Department model to store department information within a company
class Department(models.Model):
    # Foreign key to the Company model
    company = models.ForeignKey(Company, related_name='departments', on_delete=models.CASCADE)
    # Name of the department
    name = models.CharField(max_length=255)

    # Method to return the string representation of the department
    def __str__(self):
        return self.name

# Employee model to store employee information
class Employee(models.Model):
    # Foreign key to the Company model
    company = models.ForeignKey(Company, related_name='employees', on_delete=models.CASCADE)
    # Name of the employee
    name = models.CharField(max_length=255)
    # Employee ID (optional)
    employee_id = models.CharField(max_length=50, blank=True, null=True)
    # Foreign key to the Department model
    department = models.ForeignKey(Department, related_name='employees', on_delete=models.CASCADE)
    # Role of the employee
    role = models.CharField(max_length=255)
    # Date the employee started working
    date_started = models.DateField()
    # Date the employee left the company (optional)
    date_left = models.DateField(blank=True, null=True)
    # Duties of the employee
    duties = models.TextField()

    # Method to return the string representation of the employee
    def __str__(self):
        return self.name

# Role model to store role information
class Role(models.Model):
    # Name of the role
    name = models.CharField(max_length=255)

    # Method to return the string representation of the role
    def __str__(self):
        return self.name

