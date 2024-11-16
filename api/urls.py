from django.urls import path
from . import views


# const response = await axios.get("http://127.0.0.1:8000/api/fill-levels/?fill_date=YYYY-MM-DD")


urlpatterns = [ 
    path('hello/', views.say_hello),
    path('fill-levels/', views.FillLevelView.as_view(), name='fill-level-view'),
    path('weight-levels/', views.WeightLevelView.as_view(), name='weight-level-view'),
    path('fill-predictions/', views.FillPredictionView.as_view(), name='fill-prediction-view'),
    path('weight-predictions/', views.WeightPredictionView.as_view(), name='weight-prediction-view'),
]
