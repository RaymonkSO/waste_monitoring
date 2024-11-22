from datetime import datetime, time, timedelta
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from django.utils import timezone
import numpy as np
from api.models import FillLevel, WeightLevel, FillPrediction, WeightPrediction


def load_historical_data():
    csv_path = 'data/trash_bin_data.csv'
    
    try:
        df = pd.read_csv(csv_path)
        
        df['datetime'] = pd.to_datetime(df['datetime'])
        df['weekday'] = df['datetime'].dt.weekday
        df['time_of_day'] = df['datetime'].dt.time
        return df
    
    except Exception as e:
        print(f"Error loading historical data: {str(e)}")
        return None

def predict_with_historical_context(current_data, historical_df, data_type, prediction_periods):
    if len(current_data) < 2:
        return
    print("work 1 start")
    cur_weekday = current_data['datetime'].dt.weekday[0]
    historical_pattern = historical_df[historical_df['weekday'] == cur_weekday]
    print("work 1 done")
    
    historical_series = pd.Series(
        historical_pattern[f'{data_type}_level'].values,
        index=historical_pattern['datetime']
    )
    
    model = ExponentialSmoothing(
        historical_series,
        seasonal_periods=30, 
        trend='add',
        seasonal='add',
        initialization_method='estimated'
    ).fit(smoothing_level=0.6, smoothing_trend=0.3, smoothing_seasonal=0.3)
  
    print("work 2 start")
    forecast = model.forecast(prediction_periods)
    print("work 2 done")
    
    print("work 3 start")
    current_value = current_data[f'{data_type}_level'].values[-1]
    print("work 3 done")

    for i, (idx, pred) in enumerate(forecast.items()):
        forecast[idx] = 0.5 * pred + 0.5 * current_value
        forecast[idx] = max(0, min(100, forecast[idx]))
    
    return forecast

def predict_levels(models, what_to_predict: str):
    FillLevel = models['FillLevel']
    WeightLevel = models['WeightLevel']
    FillPrediction = models['FillPrediction']
    WeightPrediction = models['WeightPrediction']

    now = timezone.localtime()
    now = now.replace(hour=8, second=0, microsecond=0)
    if now.hour < 8 or now.hour > 23:
        print(now.hour)
        print("Skipping prediction outside of operational hours")
        return

    today_8am = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_11pm = now.replace(hour=23, minute=0, second=0, microsecond=0)
    
    minutes_until_11pm = (today_11pm - now).total_seconds() / 60
    prediction_periods = int(minutes_until_11pm // 30)

    if prediction_periods <= 0:
        print("Too close to closing time (11 PM). Skipping predictions.")
        return

    historical_df = load_historical_data()
    print("done loading historical data")

    current_fill_data = FillLevel.objects.all().filter(
        fill_date__gte=today_8am
    ).order_by('fill_date', 'fill_level')

    if current_fill_data.exists() and what_to_predict == 'fill':
        print("pass")
        current_fill_df = pd.DataFrame(list(current_fill_data.values()))
        current_fill_df['datetime'] = current_fill_df['fill_date']

        fill_forecast = predict_with_historical_context(
            current_fill_df,
            historical_df,
            'fill',
            prediction_periods
        )

        FillPrediction.objects.all().delete()

        for i, (_, value) in enumerate(fill_forecast.items()):
            prediction_time = (now + timedelta(minutes=30 * (i + 1))).time()
            if prediction_time <= time(23, 0):
                FillPrediction.objects.create(
                    fill_level = max(0, min(100, value)),
                    fill_time = prediction_time
                )

    # if current_weight_data.exists() and what_to_predict = 'weight':
    #     try:
    #         current_weight_df = pd.DataFrame(list(current_weight_data.values()))
    #         current_weight_df['datetime'] = current_weight_df['weight_date']
            
    #         weight_forecast = predict_with_historical_context(
    #             current_weight_df,
    #             historical_df,
    #             'weight',
    #             prediction_periods
    #         )
            
    #         # Save weight predictions
    #         WeightPrediction.objects.all().delete()
    #         for i, (_, value) in enumerate(weight_forecast.items()):
    #             prediction_time = (now + timedelta(minutes=30 * (i + 1))).time()
    #             if prediction_time <= time(23, 0):
    #                 WeightPrediction.objects.create(
    #                     weight_level=max(0, min(100, value)),
    #                     weight_time=prediction_time
    #                 )
    #     except Exception as e:
    #         print(f"Error in weight level prediction: {str(e)}")
                
    