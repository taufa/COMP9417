
import numpy as np
import pandas as pd
import matplotlib as plt
from main import NYC_LONG, NYC_LAT, MARGIN, N_ROWS

'''
Things we need to consider:
- Minimum taxi fare is $2.50 (https://www1.nyc.gov/site/tlc/passengers/taxi-fare.page)
- Passenger count must be greater than 0 (0 means the ride was either cancelled or rejected)
- Latitude and Longitude within NYC (https://www.latlong.net/place/new-york-city-ny-usa-1848.html)
'''

# longitude range
min_long = float(NYC_LONG - MARGIN)
max_long = float(NYC_LONG + MARGIN)
print(f'Longtitude: {min_long} to {max_long}')

# latitude range
min_lat = float(NYC_LAT - MARGIN)
max_lat = float(NYC_LAT + MARGIN)
print(f'Latitude: {min_lat} to {max_lat}')

def read_data():
    df = pd.read_csv('datasets/train.csv', parse_dates=['pickup_datetime'], nrows=N_ROWS)
    pd.options.display.width = 0 # display all columns

    return df

def clean_data():
    df = read_data()
    
    # remove null values
    df.dropna(inplace=True)

    # remove longitude that is out of range
    df = df[(df.pickup_longitude < max_long) & (df.pickup_longitude > min_long)]
    df = df[(df.dropoff_longitude < max_long) & (df.dropoff_longitude > min_long)]

    # remove latitude that is out of range
    df = df[(df.pickup_latitude < max_lat) & (df.pickup_latitude > min_lat)]
    df = df[(df.dropoff_latitude < max_lat) & (df.dropoff_latitude > min_lat)]

    # remove amount less than the minimum taxi fare
    df.drop(df[df.fare_amount < 2.50].index, inplace=True)

    # remove passenger count that is none
    df.drop(df[df.passenger_count <= 0].index, inplace=True)

    # split pickup datetime
    df['day'] = df['pickup_datetime'].dt.day
    df['day_of_week'] = df['pickup_datetime'].dt.dayofweek
    df['month'] = df['pickup_datetime'].dt.month
    df['year'] = df['pickup_datetime'].dt.year
    df['hour'] = df['pickup_datetime'].dt.hour

    df.drop(columns=['key', 'pickup_datetime'], inplace=True)
    

    return df

