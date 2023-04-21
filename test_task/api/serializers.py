from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Restaurant, Menu, Employee, Vote
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address']


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id', 'restaurant', 'date', 'items']


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name', 'email']


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id', 'employee', 'restaurant', 'menu']


