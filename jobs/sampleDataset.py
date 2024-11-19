import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_trash_data(start_date, num_days):
    date_rng = pd.date_range(start=start_date, 
                            end=start_date + timedelta(days=num_days), 
                            freq='15min')
    
    # Filter for time between 8 AM and 11 PM
    date_rng = [dt for dt in date_rng if dt.hour >= 8 and dt.hour < 23]
    
    df = pd.DataFrame(index=date_rng)
    df.index.name = 'datetime'
    df['day_of_week'] = df.index.dayofweek
    
    fill_level = 0
    reset_counter = 0
    fill_levels = []
    reset_counts = []
    reached_full = False
    
    for dt in df.index:
        hour = dt.hour
        day = dt.dayofweek
        
        if reached_full:
            fill_level = 0
            reset_counter += 1
            reached_full = False
        
        if day < 5:  # Weekday
            base_increase = 2 
        else:  # Weekend
            base_increase = 0.5  # Much less activity on weekends
            
        if day < 5:
            # Early morning (8-10 AM): Low activity, few students
            if 8 <= hour < 10:
                base_increase *= 0.5  # 1% - few coffee cups/breakfast items
            
            # Mid-morning (10-11:30 AM): Slightly more activity
            elif 10 <= hour < 11.5:
                base_increase *= 1.0  # 2% - normal rate
            
            # Lunch rush (11:30-2 PM): Peak activity
            elif 11.5 <= hour < 14:
                base_increase *= 4.0  # 8% - lunch containers, bottles, etc
            
            # Afternoon (2-5 PM): Moderate activity
            elif 14 <= hour < 17:
                base_increase *= 1.5  # 3% - snacks and drinks
            
            # Evening (5-11 PM): Lower activity
            else:
                base_increase *= 0.75  # 1.5% - reduced activity
        
        else:  # Weekend patterns
            # Slight increase during lunch hours
            if 11.5 <= hour < 14:
                base_increase *= 2.0  #
        
        # Add some randomness
        noise = np.random.normal(0, 0.3)
        increase = max(0, base_increase + noise)
        
        fill_level += increase
        
        if fill_level >= 100:
            fill_level = 100
            reached_full = True
        
        fill_levels.append(round(fill_level, 2))
        reset_counts.append(reset_counter)
    
    df['fill_level'] = fill_levels
    df['reset_counter'] = reset_counts
    
    return df

start_date = pd.Timestamp('2024-01-01')
df = generate_trash_data(start_date, 28)

csv_filename = 'data/trash_bin_data.csv'
df.to_csv(csv_filename)
