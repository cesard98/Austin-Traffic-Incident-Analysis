import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import contextily as ctx

# Load the GeoJSON file for Austin's districts
geojson_path = 'austin.geojson'
austin_districts = gpd.read_file(geojson_path)

# Creating the incident_count_by_district DataFrame
data = {
    'name': ['Downtown', 'Oak Hill', 'North Burnet', 'North Austin', 'St. John\'s'],
    'incident_count': [14110, 8541, 5639, 5616, 4666]
}
incident_count_by_district = pd.DataFrame(data)

# Convert it to a DataFrame with columns 'name' and 'incident_count'
incident_count_df = incident_count_by_district.copy()
incident_count_df.columns = ['name', 'incident_count']

# Merge the incident counts with the GeoDataFrame of districts
austin_districts_with_incidents = austin_districts.merge(incident_count_df, on='name', how='left')


# Convert your GeoDataFrame to Web Mercator projection
austin_districts_with_incidents = austin_districts_with_incidents.to_crs(epsg=3857)

#Plotting the choropleth map with a blue colormap
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
austin_districts_with_incidents.plot(column='incident_count', ax=ax, legend=True,
                                     legend_kwds={'label': "Number of Incidents"},
                                     cmap='Wistia', alpha=0.8)  

# Add the basemap using a different tile provider
ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)


# Enhance visibility
ax.set_axis_off()
ax.set_title('Traffic Incidents in Austin Districts')
plt.show()