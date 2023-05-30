import sys
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import contextily as cx
import shapefile as shp 
from shapely.geometry import Polygon, LineString, Point, shape, box
#philly = cx.Place("Philadelphia, PA")

bounds = [-75.280266	,39.867004,	-74.955763,	40.137992]

# https://opendataphilly.org/datasets/city-limits/

tracts = "/home/dmc7z/dev/philly/housing-characteristics/cb_2020_42_tract_500k.shp"
city_limits = "/home/dmc7z/dev/philly/housing-characteristics/City_Limits.shp"

fig, ax = plt.subplots()
fig.set_size_inches(10.0, 10.0)

data1 = gpd.read_file(tracts, bbox=bounds)
data1.plot(ax=ax)

data2 = gpd.read_file(city_limits, bbox=bounds)
xmin, ymin, xmax, ymax = data2.total_bounds
print(xmin, ymin, xmax, ymax)
pad = 0
ax.set_xlim(xmin-pad, xmax+pad)
ax.set_ylim(ymin-pad, ymax+pad)
#data2.plot(ax=ax)

#outline
#.symmetric_difference
#bounds_df = pd.concat([gdf, bounds], axis=1

geom =box(*data2.total_bounds)
#print(geom)

#zip(-75.280266, 39.867004, -74.955763, 40.137992)
#sys.exit()

#geometry = [box(x1, y1, x2, y2) for x1,y1,x2,y2 in zip(-75.280266, 39.867004, -74.955763, 40.137992)]
#df = df.drop(['left', 'bottom', 'right', 'top'], axis=1)
geodf = gpd.GeoDataFrame({ "geometry": geom }, index=[0], crs="EPSG:4326")

outline = geodf.overlay(data2, how='symmetric_difference')
outline.plot(ax=ax, color="white")
plt.show()
