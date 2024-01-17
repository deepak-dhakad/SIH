import random
import datetime
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from kerastuner.tuners import RandomSearch
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

parking_df = pd.read_csv('C:\SIH\Dynamic_pricing\parking.csv')

X = parking_df[['Occupied', 'Timestamp', 'Demand']].copy()
X['Timestamp'] = pd.to_datetime(X['Timestamp'])
X['Hour'] = X['Timestamp'].dt.hour
X['DayOfWeek'] = X['Timestamp'].dt.dayofweek
X.drop(columns=['Timestamp'], inplace=True)
y = parking_df['Price'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

def build_model(hp):
    model = keras.Sequential()
    model.add(layers.Dense(units=hp.Int('units', min_value=32, max_value=512, step=32), activation='relu', input_dim=X_train.shape[1]))
    model.add(layers.Dense(1))
    model.compile(optimizer=keras.optimizers.Adam(learning_rate=hp.Choice('learning_rate', values=[1e-2, 1e-3, 1e-4])),
                  loss='mse', metrics=['mae'])
    return model

tuner = RandomSearch(build_model, objective='val_loss', max_trials=10, directory='C:\SIH\Dynamic_pricing\parking_tuning', project_name='parking_model')

tuner.search(X_train, y_train, epochs=10, validation_split=0.2)

best_hps = tuner.get_best_hyperparameters(num_trials=1)[0]

best_model = tuner.hypermodel.build(best_hps)

best_model.fit(X_train, y_train, epochs=50, validation_split=0.2, verbose=0)

y_pred = best_model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print(f"Root Mean Squared Error: {rmse}")
print(f"R-squared: {r2}")
import joblib
joblib.dump(best_model, 'C:\SIH\Dynamic_pricing\parking_price_prediction_model.pkl')