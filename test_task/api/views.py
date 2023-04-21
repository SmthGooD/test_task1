from django.shortcuts import render
from rest_framework import viewsets, generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Restaurant, Menu, Employee, Vote
from .serializers import RestaurantSerializer, MenuSerializer, EmployeeSerializer, VoteSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        date = self.request.query_params.get('date', None)
        if date is not None:
            queryset = queryset.filter(date=date)
        else:
            queryset = queryset.filter(date=timezone.now().date())
        return queryset


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer



@api_view(['POST'])
def vote(request):
    build_version = request.headers.get('X-Build-Version')
    if build_version == '1.0':
        employee_id = request.data.get('employee_id')
        restaurant_id = request.data.get('restaurant_id')
        menu_id = request.data.get('menu_id')
    else:
        employee_id = request.data.get('employee')
        restaurant_id = request.data.get('restaurant')
        menu_id = request.data.get('menu')
    employee = get_object_or_404(Employee, id=employee_id)
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    menu = get_object_or_404(Menu, id=menu_id)
    votes = Vote.objects.create(employee=employee, restaurant=restaurant, menu=menu)
    serializer = VoteSerializer(votes)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def results(request):
    menu = Menu.objects.filter(date=timezone.now().date()).first()
    if menu is None:
        return Response({'message': 'No menu found for today'}, status=status.HTTP_404_NOT_FOUND)
    votes = Vote.objects.filter(menu=menu)
    results = {}
    for vote in votes:
        if vote.restaurant in results:
            results[vote.restaurant] += 1
        else:
            results[vote.restaurant] = 1
    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
    return Response(sorted_results)






