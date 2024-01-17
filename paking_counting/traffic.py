import pandas as pd
import random
from datetime import datetime
import time
import warnings

def read_empty_slots():
    with open(r'C:\SIH\paking_counting\empty_slots.txt', 'r') as file:
        empty_slots_str = file.read()
    return list(map(int, empty_slots_str.split(',')))

def update_empty_slots_file(empty_slots):
    with open(r'C:\SIH\paking_counting\empty_slots.txt', 'w') as file:
        file.write(','.join(map(str, empty_slots)))

def read_csv_entries(csv_file_path):
    df = pd.read_csv(csv_file_path)
    return df.iterrows()

output_data = pd.DataFrame(columns=['Fastag_Number', 'Vehicle_Number', 'Slot_Number', 'Current_Time'])

def update_excel_sheet(entry, empty_slots):
    fastag_number = entry['Fastag_Number']
    vehicle_number = entry['Vehicle_Number']
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    slot_number = random.choice(empty_slots)
    
    empty_slots.remove(slot_number)
    update_empty_slots_file(empty_slots)
    
    new_data = pd.DataFrame({'Fastag_Number': [fastag_number],
                             'Vehicle_Number': [vehicle_number],
                             'Slot_Number': [slot_number],
                             'Current_Time': [current_time]})

    global output_data
    output_data = pd.concat([new_data, output_data], ignore_index=True)

    print(f"Saved entry for Fastag_Number: {fastag_number}, Vehicle_Number: {vehicle_number}, Slot_Number: {slot_number}")

csv_file_path = r'C:\SIH\paking_counting\random_tag.csv'
excel_file_path = r'C:\SIH\paking_counting\output.xlsx'
excel_sheet_name = 'Sheet1'

warnings.simplefilter(action='ignore', category=FutureWarning)

empty_slots = read_empty_slots()
for _, entry in read_csv_entries(csv_file_path):
    if empty_slots:
        update_excel_sheet(entry, empty_slots)
        time.sleep(3)

output_data.to_excel(excel_file_path, sheet_name=excel_sheet_name, index=False)
print("All entries saved. Exiting the program.")
