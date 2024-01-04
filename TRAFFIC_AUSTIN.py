import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import HeatMap
import geopandas as gpd
from shapely.geometry import Point

# Load the dataset
file_path = 'Real-Time_Traffic_Incident_Reports_20231226.csv'
traffic_data = pd.read_csv(file_path)

# Convert 'Published Date' to datetime and extract year, month, day, and hour
traffic_data['Published Date'] = pd.to_datetime(traffic_data['Published Date'], errors='coerce')
traffic_data = traffic_data.dropna(subset=['Published Date'])
traffic_data['Year'] = traffic_data['Published Date'].dt.year
traffic_data['Month'] = traffic_data['Published Date'].dt.month
traffic_data['DayOfWeek'] = traffic_data['Published Date'].dt.dayofweek
traffic_data['Hour'] = traffic_data['Published Date'].dt.hour

# Incident Type Analysis: Count incidents by type
incident_type_counts = traffic_data['Issue Reported'].value_counts()

# Temporal Analysis: Count incidents by time units
yearly_counts = traffic_data.groupby('Year')['Issue Reported'].count()
monthly_counts = traffic_data.groupby('Month')['Issue Reported'].count()
dayofweek_counts = traffic_data.groupby('DayOfWeek')['Issue Reported'].count()
hourly_counts = traffic_data.groupby('Hour')['Issue Reported'].count()

# Spatial Analysis: Generate a heatmap
valid_coords = traffic_data.dropna(subset=['Latitude', 'Longitude'])
austin_center = [30.2672, -97.7431]  # Latitude and Longitude of Austin, TX
##sampled_data = valid_coords.sample(n=10000, random_state=1)
austin_map = folium.Map(location=austin_center, zoom_start=12)
##heat_data_sampled = [[row['Latitude'], row['Longitude']] for index, row in sampled_data.iterrows()]
heat_data_sampled = [[row['Latitude'], row['Longitude']] for index, row in valid_coords.iterrows()]
HeatMap(heat_data_sampled, radius=10).add_to(austin_map)
heatmap_file_path = 'austin_traffic_heatmap.html'
austin_map.save(heatmap_file_path)

# Frequent Locations Analysis: Identify common addresses and coordinate clusters
top_locations = traffic_data['Address'].value_counts().head(10)
top_coordinates = valid_coords.groupby(['Latitude', 'Longitude']).size().reset_index(name='Counts')
top_coordinates = top_coordinates.sort_values(by='Counts', ascending=False).head(10)

# Output results (can be replaced with print statements or further processing)
print(incident_type_counts, yearly_counts, monthly_counts, dayofweek_counts, hourly_counts, top_locations, top_coordinates)

# Note: This code is a template and may require adjustments based on the specific format and contents of your dataset.