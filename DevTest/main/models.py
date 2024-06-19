from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=False)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=False)
    email = models.EmailField(max_length=1000, blank=False)
    phone_number = models.CharField(max_length=20)

    @property
    def full_name(self):
        return f"{self.first_name} {self.middle_name} {self.surname}"


class Company(models.Model):
    name = models.CharField(max_length=255)
    registration_date = models.DateField()
    registration_number = models.CharField(max_length=50)
    address = models.TextField()
    contact_person = models.CharField(max_length=255)
    number_of_employees = models.IntegerField()
    contact_phone = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.name
    

class Department(models.Model):
    company = models.ForeignKey(Company, related_name='departments', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Employee(models.Model):
    company = models.ForeignKey(Company, related_name='employees', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    employee_id = models.CharField(max_length=50, blank=True, null=True)
    department = models.ForeignKey(Department, related_name='employees', on_delete=models.CASCADE)
    role = models.CharField(max_length=255)
    date_started = models.DateField()
    date_left = models.DateField(blank=True, null=True)
    duties = models.TextField()

    def __str__(self):
        return self.name
    

class Role(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

