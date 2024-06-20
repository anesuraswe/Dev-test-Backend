from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'employees', views.EmployeeViewSet, basename='employee')
router.register(r'companies', views.CompanyViewSet, basename='company')
router.register(r'departments', views.DepartmentViewSet, basename='department')
router.register(r'roles', views.RoleViewSet, basename='role')


urlpatterns = [
    path('api/', include(router.urls)),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
]
