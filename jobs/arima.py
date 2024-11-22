import pandas as pd
import numpy as np
from datetime import datetime
from statsmodels.tsa.arima.model import ARIMA
from api.models import FillLevel, FillPrediction
import pickle


def load_data(filldf):
    df = filldf.copy()
    df['day_of_week'] = df['fill_date'].dt.weekday
    df['hour'] = df['fill_date'].dt.hour
    return df

def forecast_hourly_fill_level(history, arima_order):
    if len(history) < max(arima_order):
        return 0  
    
    with open('param/arima_5_1_0.pkl', 'rb') as file:
        saved_params = pickle.load(file)

    min_points = 119 # 17 hr x 7 days
    recent_data = history[:min_points]
    
    model = ARIMA(recent_data, order=saved_params['order'])
    model_fit = model.fit(start_params=saved_params['params'])

    forecast = model_fit.forecast(steps=1)
    return max(forecast[0], 0) 

def save_prediction(predictions: pd.DataFrame):
    for i, row in predictions.iterrows():
        FillPrediction.objects.create(
            fill_date=row['timestamp'],
            fill_level=row['predicted_fill_level']
        )
    

def predict_bin_fill_today():
    current_time = datetime.now()
    query_set = FillLevel.objects.all()

    FillPrediction.objects.all().delete()

    prod_df = pd.DataFrame(list(query_set.values()))
    prod_df = prod_df[['fill_level', 'fill_date']]

    prod_df['fill_level'] = pd.to_numeric(prod_df['fill_level'], errors='coerce')
    prod_df['fill_level'] = prod_df['fill_level'].astype(float)
    prod_df['fill_date'] = pd.to_datetime(prod_df['fill_date'])

    df = load_data(prod_df)

    is_weekday = current_time.weekday() < 5
    arima_order = (5, 1, 0) if is_weekday else (3, 1, 0)

    historical_data = df[df['day_of_week'] < 5] if is_weekday else df[df['day_of_week'] >= 5]
    today_data = df[df['fill_date'].dt.date == current_time.date()]

    predictions = []
    prediction_timestamps = []
    full_empty_events = []

    start_hour = current_time.hour + 1
    last_hour_data = today_data[today_data['hour'] == current_time.hour - 8]['fill_level'].mean()
    last_hour_data = last_hour_data if not np.isnan(last_hour_data) else 0 

    second_last_hour_data = today_data[today_data['hour'] == current_time.hour - 1 - 8]['fill_level'].mean()
    second_last_hour_data = last_hour_data if not np.isnan(last_hour_data) else 0

    today_slope = last_hour_data - second_last_hour_data if last_hour_data < second_last_hour_data else last_hour_data * 0.1
    for hour in range(start_hour, 23):
        historical_hourly_data = historical_data[historical_data['hour'] == hour]['fill_level'].tolist()
        arima_forecast = forecast_hourly_fill_level(historical_hourly_data, arima_order)

        forecast = 0.5 * arima_forecast + 0.5 * last_hour_data + 0.5 * today_slope

        # print("Hour : " , hour)
        # print(last_hour_data)
        # print(arima_forecast)
        # print("baseline prediction (without slope): ", arima_forecast * 0.5 + last_hour_data * 0.5)
        # print(today_slope)

        # Append predictions
        current_day_time = current_time.replace(hour=hour, minute=0, second=0)
        predictions.append(min(forecast, 100)) 
        prediction_timestamps.append(current_day_time)

    forecast_df = pd.DataFrame({
        'timestamp': prediction_timestamps,
        'predicted_fill_level': predictions
    })

    save_prediction(forecast_df)
    print("Saved Predictions")

# def saveall():
#     df = pd.read_csv("jobs/fill_level_data.csv")
#     for timestamp, fill_level in df.values:
#         FillLevel.objects.create(fill_date=timestamp, fill_level=fill_level)
#     print("saved all records")
#     print(df.head())

def deleteall():
    FillPrediction.objects.all().delete()
    FillLevel.objects.all().delete()
    print("Deleted all records")


