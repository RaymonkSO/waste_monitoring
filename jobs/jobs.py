import requests
from api.models import FillLevel, WeightLevel, FillPrediction, WeightPrediction
from .prediction import predict_levels

# https://api.thingspeak.com/channels/2669837/fields/2.json?api_key=MFOMLJJL1QN5UJ67&results=2
THINGSPEAK_API_URL = "https://api.thingspeak.com/channels/"
CHANNEL_ID = 2669837

WEIGHT_API_KEY = "P3JO4HPITSP8GBFQ"
FILL_API_KEY = "MFOMLJJL1QN5UJ67"

THINGSPEAK_WEIGHT_URL = f"{THINGSPEAK_API_URL}{CHANNEL_ID}/fields/1.json?api_key={WEIGHT_API_KEY}"
THINGSPEAK_FILL_URL = f"{THINGSPEAK_API_URL}{CHANNEL_ID}/fields/2.json?api_key={FILL_API_KEY}"



def schedule_api_call_fill():

    models ={
    'FillLevel': FillLevel,
    'WeightLevel': WeightLevel,
    'FillPrediction': FillPrediction,
    'WeightPrediction': WeightPrediction
    }
    
    response = requests.get(THINGSPEAK_FILL_URL)
    response.raise_for_status()
    data = response.json()['feeds']

    data_updated = False

    for entry in data:
        cur_level = entry['field2']
        cur_date = entry['created_at']
        print(entry)
        try:
            existing_entry = FillLevel.objects.get(fill_date=cur_date)
            if float(existing_entry.fill_level) != float(cur_level):
                existing_entry.fill_level = cur_level
                print("Fetched and merged data from ThingSpeak API for fill level")
                existing_entry.save(update_fields=['fill_level'])

                data_updated = True
        except FillLevel.DoesNotExist:
            if cur_level is not None:
                print("Added new data for fill level")
                FillLevel.objects.create(
                    fill_level=cur_level,
                    fill_date=cur_date
                )
                data_updated = True
    
    if data_updated:
        predict_levels(models, 'fill')
        print("Updated Predicted fill levels")


def schedule_api_call_weight():

    models ={
    'FillLevel': FillLevel,
    'WeightLevel': WeightLevel,
    'FillPrediction': FillPrediction,
    'WeightPrediction': WeightPrediction
    }

    response = requests.get(THINGSPEAK_WEIGHT_URL)
    response.raise_for_status()
    data = response.json()['feeds']
    for entry in data:
        cur_level = entry['field1']
        cur_date = entry['created_at']
        try:
            existing_entry = WeightLevel.objects.get(weight_date=cur_date)
            if float(existing_entry.weight_level) != float(cur_level):
                existing_entry.weight_level = cur_level
                existing_entry.save(update_fields=['weight_level'])
        except WeightLevel.DoesNotExist:
            if cur_level is not None:
                WeightLevel.objects.create(
                    weight_level=cur_level,
                    weight_date=cur_date
                )
                print("Added new data for weight level")






