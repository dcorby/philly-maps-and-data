import geopandas as gpd
import contextily as cx
import json
import sys

base_dir = "/home/dmc7z/dev/philly/pages/districts"

def main():
    """
    Parse the shapefiles and extract their intersections with Philly city limits
    Write a geojson file for each of the shapefiles
    """

    # Get a contextily Place object, and get the bounds
    #philly = cx.Place("Philadelphia, PA")
    #bounds = philly.bbox
    #print(bounds)
    bounds = [-75.2802977, 39.867005, -74.9558314, 40.1379593]

    # Get the city limits data frame, used to sjoin the districts
    gdf_limits = gpd.read_file(f"{base_dir}/data/City_Limits.shp", bbox=bounds).to_crs("EPSG:4326")

    # Iterate over shapefiles, sjoining each with the city limits data frame
    shapefiles = {
      "City Council": "GIS_PLANNING_Council_Districts_2016",
      "PA House": "Pennsylvania_House_of_Representatives_Districts",
      "PA Senate": "Pennsylvania_Senate_Districts",
      "US Congress": "U.S._Congressional_Districts_for_Pennsylvania"
    }

    geojson = {}
    for shapefile in shapefiles:
        pathname = f"{base_dir}/data/{shapefiles[shapefile]}.shp"
        print(f"Processing shapefile for {shapefile} ({pathname})...")

        # Load the data frame
        gdf = gpd.read_file(pathname, engine="fiona").to_crs("EPSG:4326")
        
        # Do some cleaning
        if shapefile == "US Congress":
            gdf = gdf[ (gdf["LEG_DISTRI"] != 1) & (gdf["LEG_DISTRI"] != 4) ]
        elif shapefile == "PA House":
            gdf = gdf[ (gdf["LEG_DISTRI"] != 162) & (gdf["LEG_DISTRI"] != 142) & (gdf["LEG_DISTRI"] != 18) & (gdf["LEG_DISTRI"] != 152) & (gdf["LEG_DISTRI"] != 153) & (gdf["LEG_DISTRI"] != 154) & (gdf["LEG_DISTRI"] != 166) & (gdf["LEG_DISTRI"] != 148) & (gdf["LEG_DISTRI"] != 164) ]
        elif shapefile == "PA Senate":
            gdf = gdf[ (gdf["LEG_DISTRI"] != 17) & (gdf["LEG_DISTRI"] != 26) & (gdf["LEG_DISTRI"] != 12) & (gdf["LEG_DISTRI"] != 6) ]

        # Sjoin it and store it
        gdf = gpd.sjoin(gdf, gdf_limits)
        geojson[shapefile.lower().replace(" ", "-")] = json.loads(gdf.to_json())

    pathname = f"{base_dir}/districts.geojson"
    print(f"Writing districts geojson to {pathname}...")
    with open(pathname, "w") as f:
        json_str = json.dumps(geojson)
        f.write(json_str)  

    pathname = f"{base_dir}/city-limits.geojson"
    print(f"Writing city limits geojson to {pathname}...")
    with open(pathname, "w") as f:
        f.write(gdf_limits.to_json())  

if __name__ == "__main__":
    main()
