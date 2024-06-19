from django.test import TestCase

# Create your tests here.

from .models import Company

class CompanyModelTest(TestCase):
    def test_string_representation(self):
        company = Company(name="Test Company")
        self.assertEqual(str(company), company.name)
