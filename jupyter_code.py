
import gmaps
import pandas as pd
import gmaps.datasets

gmaps.configure(api_key='')

noise_pol = pd.read_csv('avg.csv')
weights = noise_pol['noise index']
locations = noise_pol[['latitude', 'longitude']]

fig = gmaps.figure()
fig.add_layer(gmaps.heatmap_layer(locations, weights=weights))
fig