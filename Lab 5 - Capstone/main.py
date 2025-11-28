import os
import pandas as pd
import matplotlib.pyplot as plt

class MeterReading:
    def __init__(self, timestamp, kwh):
        self.timestamp = timestamp
        self.kwh = kwh

class Building:
    def __init__(self, name):
        self.name = name
        self.readings = []

    def add_reading(self, reading):
        self.readings.append(reading)

class BuildingManager:
    def __init__(self):
        self.buildings = []
    
    def add_building(self, building):
        self.buildings.append(building)

master_df = pd.DataFrame()
data_path = 'data'

if not os.path.exists(data_path):
    print("Error: 'data' folder not found. Please create it and add CSV files.")
    exit()

print("Processing files...")
for file in os.listdir(data_path):
    if file.endswith(".csv"):
        try:
            # Read CSV
            file_path = os.path.join(data_path, file)
            df = pd.read_csv(file_path)
            
            # Add metadata (Building Name from filename)
            df['building'] = file.split('_')[0]
            master_df = pd.concat([master_df, df], ignore_index=True)
            
        except Exception as e:
            # [cite_start]Handle exceptions [cite: 22-24]
            print(f"Skipping corrupt file {file}: {e}")

if master_df.empty:
    print("No valid data found.")
    exit()

# Ensure timestamp is datetime
master_df['timestamp'] = pd.to_datetime(master_df['timestamp'])

# Daily Totals
daily_df = master_df.groupby(['building', master_df['timestamp'].dt.date])['kwh'].sum().reset_index()

# Building Summary (Mean, Min, Max)
summary_df = master_df.groupby('building')['kwh'].agg(['sum', 'mean', 'min', 'max']).reset_index()

manager = BuildingManager()
for name in master_df['building'].unique():
    b = Building(name)
    subset = master_df[master_df['building'] == name]
    # Add readings to object
    for _, row in subset.iterrows():
        b.add_reading(MeterReading(row['timestamp'], row['kwh']))
    manager.add_building(b)

plt.figure(figsize=(10, 8))

# 1. Trend Line
plt.subplot(2, 2, 1)
for b in daily_df['building'].unique():
    d = daily_df[daily_df['building'] == b]
    plt.plot(d['timestamp'], d['kwh'], label=b)
plt.title("Daily Trends")
plt.legend()

# 2. Bar Chart
plt.subplot(2, 2, 2)
plt.bar(summary_df['building'], summary_df['mean'])
plt.title("Avg Weekly Usage")

# 3. Scatter Plot
plt.subplot(2, 2, 3)
plt.scatter(master_df['timestamp'], master_df['kwh'], alpha=0.5)
plt.title("Peak Load")

if not os.path.exists('output'):
    os.makedirs('output')
plt.savefig('output/dashboard.png')

master_df.to_csv('output/cleaned_energy_data.csv', index=False)
summary_df.to_csv('output/building_summary.csv', index=False)

top_b = summary_df.loc[summary_df['sum'].idxmax()]
report = f"""
EXECUTIVE SUMMARY
-----------------
Total Consumption: {master_df['kwh'].sum():.2f}
Highest Consumer: {top_b['building']} ({top_b['sum']:.2f})
Peak Load: {master_df['kwh'].max():.2f}
"""

with open('output/summary.txt', 'w') as f:
    f.write(report)

print("Pipeline complete. Output saved to /output/")
