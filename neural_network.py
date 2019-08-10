
import numpy as np
import math
from keras.models import Sequential
from keras.layers import Dense
from preprocess import clean_data
from haversine import haversine, Unit
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import scale

df = clean_data()

def euclidean_distance(long1, lat1, long2, lat2):
    distance = pow(pow((long1 - long2), 2) + pow((lat1 - lat2), 2), 0.5)
    return distance
    
def haversine_distance(df):
    pickup_location = (df['pickup_longitude'], df['pickup_latitude'])
    dropoff_location = (df['dropoff_longitude'], df['dropoff_latitude'])
    distance = haversine(pickup_location, dropoff_location)
    return distance

df['distance'] = df.apply(haversine_distance, axis=1)
df.drop(columns=['pickup_longitude', 'pickup_latitude', 'dropoff_longitude', 'dropoff_latitude'], inplace=True)
print(df.head())

# split into input (X) and output (y) variables
train_set = df[['passenger_count', 'day', 'day_of_week', 'month', 'year', 'hour',  'distance']]
target_set = df[['fare_amount']]

#df_scaled = scale(train_set)

# split to 80% training set and 20% testing set
X_train, X_test, y_train, y_test = train_test_split(train_set, target_set, test_size=0.2)

# define the keras model
model = Sequential()
model.add(Dense(128, activation= 'relu', input_dim=X_train.shape[1]))
model.add(Dense(64, activation= 'relu'))
model.add(Dense(32, activation= 'relu'))
model.add(Dense(8, activation= 'relu'))
model.add(Dense(1))

model.summary()

### compile the keras model
##model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.compile(loss='mse', optimizer='adam', metrics=['mse'])
##
### fit the keras model on the dataset
##model.fit(train_set, target_set, epochs=500, batch_size=100)
model.fit(X_train, y_train, epochs=1)

### evaluate the keras model
_, accuracy = model.evaluate(X_train, y_train)
print(f'Accuracy: {accuracy}')

def predict_random(df, X_test, model):
    sample = X_test.sample(n=1, random_state=np.random.randint(low=0, 
                                                              high=10000))
    idx = sample.index[0]
  
    actual_fare = df.loc[idx,'fare_amount']
    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 
                 'Saturday', 'Sunday']
    day_of_week = day_names[df.loc[idx,'day_of_week']]
    hour = df.loc[idx,'hour']
    predicted_fare = model.predict(sample)[0][0]
    rmse = np.sqrt(np.square(predicted_fare-actual_fare))

    print("Trip Details: {}, {}:00hrs".format(day_of_week, hour))  
    print("Actual fare: ${:0.2f}".format(actual_fare))
    print("Predicted fare: ${:0.2f}".format(predicted_fare))
    print("RMSE: ${:0.2f}".format(rmse))

predict_random(df, X_test, model)
