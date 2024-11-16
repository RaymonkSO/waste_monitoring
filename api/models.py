from django.db import models


class FillLevel(models.Model):
    fill_level = models.FloatField(null=True, blank=False)
    fill_date = models.DateTimeField(auto_now_add=False)

    def __str__(self):
        return str(self.fill_date) + " " + str(self.fill_level)

class WeightLevel(models.Model):
    weight_level = models.FloatField(null=True, blank=False)
    weight_date = models.DateTimeField(null=True, blank=False) # datetime.datetime

    def __str__(self):
        return str(self.weight_date) + " " + str(self.weight_level)
    
class FillPrediction(models.Model):
    fill_level = models.FloatField(null=True, blank=False)
    fill_time = models.TimeField(auto_now_add=False)

    def __str__(self):
        return str(self.fill_time) + " " + str(self.fill_level)

class WeightPrediction(models.Model):
    weight_level = models.FloatField(null=True, blank=False)
    weight_time = models.TimeField(auto_now_add=False)

    def __str__(self):
        return str(self.weight_time) + " " + str(self.weight_level)