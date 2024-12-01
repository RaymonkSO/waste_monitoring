from rest_framework import serializers
from .models import FillLevel, WeightLevel, FillPrediction, WeightPrediction

class FillLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FillLevel
        fields = '__all__'

class WeightLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeightLevel
        fields = '__all__'

class FillPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FillPrediction
        fields = '__all__'

class WeightPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeightPrediction
        fields = '__all__'
