from django.contrib import admin
from .models import FillLevel, WeightLevel, FillPrediction, WeightPrediction

# Register your models here.
admin.site.register(FillLevel)
admin.site.register(WeightLevel)
admin.site.register(FillPrediction)
admin.site.register(WeightPrediction)