from rest_framework import serializers
from .models import FillLevel, WeightLevel

class FillLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FillLevel
        fields = '__all__'

class WeightLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeightLevel
        fields = '__all__'