'''
LIBRARIES
'''

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

income = pd.read_csv('output/data.csv')
income = income.rename(columns = {'Country Code':'iso_a3'})

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

df = world.merge(income, how='left')

ax = df.plot(column='Income', cmap='Purples', scheme='quantiles', legend=False, figsize=(15, 10), missing_kwds={"color": "lightgrey", "label": "Missing values",})
ax.set_axis_off()
ax.set_facecolor("yellow")
plt.show()



