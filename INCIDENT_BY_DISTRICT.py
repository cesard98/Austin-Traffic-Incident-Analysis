import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Load the traffic incident data
file_path = 'Real-Time_Traffic_Incident_Reports_20231226.csv'
traffic_data = pd.read_csv(file_path)

# Convert 'Published Date' to datetime and filter for valid coordinates
traffic_data['Published Date'] = pd.to_datetime(traffic_data['Published Date'], errors='coerce')
traffic_data = traffic_data.dropna(subset=['Latitude', 'Longitude', 'Published Date'])

# Convert traffic incident data to a GeoDataFrame
crs = 'EPSG:4326'  # Coordinate Reference System: WGS84
geometry = [Point(xy) for xy in zip(traffic_data['Longitude'], traffic_data['Latitude'])]
geo_traffic_data = gpd.GeoDataFrame(traffic_data, crs=crs, geometry=geometry)

# Load the GeoJSON file for Austin's districts
geojson_path = 'austin.geojson'
austin_districts = gpd.read_file(geojson_path)

# Ensure both GeoDataFrames are using the same CRS
austin_districts = austin_districts.to_crs(crs)

# Perform a spatial join to associate each traffic incident with a district
joined_data = gpd.sjoin(geo_traffic_data, austin_districts, how='inner', predicate='within')

# Count the number of incidents in each district (replace 'district_column_name' with actual column name)
incident_count_by_district = joined_data['name'].value_counts().head(5)

# Output the results
print(incident_count_by_district)