import random
import datetime
import pandas as pd

start_date = datetime.date(2023, 1, 1)
end_date = datetime.date(2023, 9, 30)
num_days = (end_date - start_date).days
num_hours_per_day = 24
num_parking_spots = 396
user_count = 1000
max_stay_duration_hours = 8

date_rng = pd.date_range(start=start_date, end=end_date, freq='H')

data = {
    'Timestamp': [],
    'Occupied': [],
    'Price': [],
    'User_ID': [],
    'Demand': [],
}

initial_base_price = 60

for timestamp in date_rng:
    occupied_spots = random.randint(0, num_parking_spots)
    demand_multiplier = random.randint(1, 10)
    occupancy_percentage = occupied_spots / num_parking_spots
    
    price_multiplier = initial_base_price + (occupancy_percentage * 40) + random.uniform(-10, 10)
    
    if price_multiplier < 65:
        price_multiplier += random.uniform(0, 5)
    
    if price_multiplier > 95:
        price_multiplier -= random.uniform(0, 5)
    
    price = max(min(price_multiplier, 100), 60)
    
    user_id = random.randint(1, user_count)

    if random.random() < 0.2:
        stay_duration = random.randint(1, max_stay_duration_hours)
        exit_time = timestamp + datetime.timedelta(hours=stay_duration)

        if random.random() < 0.2:
            user_id = random.randint(1, user_count)

        data['Timestamp'].append(timestamp)
        data['Occupied'].append(occupied_spots)
        data['Price'].append(price)
        data['User_ID'].append(user_id)
        data['Demand'].append(demand_multiplier)

    if len(data['Timestamp']) >= 2000:
        break

parking_df = pd.DataFrame(data)

parking_df.to_csv('parking.csv', index=False)

print("Generated parking data with demand and adjusted pricing range (60 to 100) saved to 'parking.csv'.")
