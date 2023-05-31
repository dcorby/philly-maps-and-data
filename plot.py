import sys
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import contextily as cx
import shapefile as shp 
from shapely.geometry import Polygon, LineString, Point, shape, box
import parse
from mpl_toolkits.axes_grid1 import make_axes_locatable

"""
Creating legend is weird in Geopandas. Some resources:
https://stackoverflow.com/questions/36008648/colorbar-on-geopandas
https://stackoverflow.com/questions/8342549/add-colorbar-to-a-sequence-of-line-plots/11558629#11558629
https://stackoverflow.com/questions/43442925/color-coding-using-scalar-mappable-in-matplotlib
"""

data_dir = "/home/dmc7z/dev/philly/data/housing-characteristics/"

"""
Census tracts: https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.2020.html#list-tab-1883739534
City limits: https://opendataphilly.org/datasets/city-limits/
Bounds:
  >>> philly = cx.Place("Philadelphia, PA")
  >>> bounds = philly.bounds
"""
bounds = [-75.280266, 39.867004, -74.955763, 40.137992]
tracts = f"{data_dir}/cb_2020_42_tract_500k.shp"
limits = f"{data_dir}/City_Limits.shp"

fig, ax = plt.subplots()
fig.set_size_inches(10.0, 10.0)

gdf_tracts = gpd.read_file(tracts, bbox=bounds, crs="EPSG:4326").to_crs("EPSG:4326")
gdf_limits = gpd.read_file(limits, bbox=bounds, crs="EPSG:4326").to_crs("EPSG:4326")
gdf_inter = gpd.clip(gdf_tracts, gdf_limits)

fields, gdf_houses = parse.get()
gdf_inter = pd.merge(gdf_inter, gdf_houses[["geography", "mean"]], left_on="AFFGEOID", right_on="geography", how="left").drop(columns=["geography"])

sm = plt.cm.ScalarMappable(cmap="OrRd", norm=plt.Normalize(vmin=0, vmax=9))
sm.set_array([])

# Make colorbar the same height as the plot
# https://stackoverflow.com/questions/18195758/set-matplotlib-colorbar-size-to-match-graph
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)
cbar = plt.colorbar(sm, ticks=range(0,9+1), aspect=10, orientation="vertical", label="Avg Year Built", cax=cax)
#cbar = plt.colorbar(sm, ticks=range(0,9+1), aspect=10, orientation="vertical", ax=ax, label="Avg Year Built")

cbar.ax.set_yticklabels(fields)

gdf_inter.plot(ax=ax, edgecolor="black", missing_kwds={ "color": "gray" }, lw=0.5, column="mean", cmap="OrRd", legend=False)
plt.suptitle("Philadelphia, ACS Selected Housing Characteristics, \nYear Structure Built - 2020 Census Tracts", fontsize=15, y=0.90)
plt.tight_layout()
#plt.figtext(0.99, 0.01, 'footnote text', horizontalalignment='left')
plt.show()
