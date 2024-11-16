from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


from django_filters import rest_framework as filters
from rest_framework import viewsets, generics

from .models import FillLevel, WeightLevel
from .serializers import FillLevelSerializer, WeightLevelSerializer
import json

class FillLevelFilter(filters.FilterSet):
    fill_date = filters.DateFilter(field_name='fill_date', lookup_expr='date')
    class Meta:
        model = FillLevel
        fields = ['fill_date']


class FillLevelView(generics.ListAPIView):
    queryset = FillLevel.objects.all()
    serializer_class = FillLevelSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = FillLevelFilter
    
class WeightLevelFilter(filters.FilterSet):
    weight_date = filters.DateFilter(field_name='weight_date', lookup_expr='date')
    class Meta:
        model = WeightLevel
        fields = ['weight_date']

class WeightLevelView(generics.ListAPIView):
    queryset = WeightLevel.objects.all()
    serializer_class = WeightLevelSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = WeightLevelFilter


@csrf_exempt
def say_hello(request):
    return HttpResponse('Hello World')

