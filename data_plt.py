from utils import *

from siphon.radarserver import RadarServer
from datetime import datetime, timedelta
from matplotlib.animation import ArtistAnimation, PillowWriter
from IPython.display import HTML
import matplotlib
import metpy.plots as mpplots
import cartopy.feature as cfeature
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature

import matplotlib.pyplot as plt

def create_plot(widget_box):
    dt1, dt2, lon_1, lon_2, lon_3, lat_1, lat_2, lat_3 = widget_values(widget_box)

    # Quick check to see if the user selected a time
    if dt1 == dt2:
        dt2 = dt1 + timedelta(minutes=30)

    # Load in radar data and variables https://tds-nexrad.scigw.unidata.ucar.edu/thredds/catalog/catalog.html
    rs = RadarServer('http://tds-nexrad.scigw.unidata.ucar.edu/thredds/radarServer/nexrad/level2/S3/')  # Access THREDDS for data files
    query = rs.query()
    query.lonlat_point(lon_3, lat_3).time_range(dt1, dt2)

    # Get the colortable and norm for the data
    ref_norm, ref_cmap = mpplots.ctables.registry.get_with_steps('NWSReflectivity', 5, 5)

    # Iterate over the catalog and remotely access the data
    cat = rs.get_catalog(query)
    ds = cat.datasets[0]
    data = ds.remote_access()
    fig = plt.figure(figsize=(10, 7.5))
    ax = new_map(fig, data.StationLongitude, data.StationLatitude)

    # Set limits in lat/lon space
    ax.set_extent([lon_1, lon_2, lat_1, lat_2])

    # Add map features
    ax.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '50m', edgecolor='face', facecolor='#020514'))
    ax.add_feature(cfeature.NaturalEarthFeature('physical', 'ocean', '50m', edgecolor='face', facecolor='#bbcfda'))
    ax.add_feature(cfeature.LAKES, facecolor='blue', edgecolor='white', alpha=0, zorder=12)
    ax.add_feature(cfeature.STATES.with_scale('50m'), edgecolor='white', linewidth=0.2, zorder=11)
    ax.add_feature(cfeature.BORDERS.with_scale('50m'), edgecolor='white', linewidth=0.4, zorder=11)
    ax.add_feature(cfeature.COASTLINE.with_scale('50m'), edgecolor='white', linewidth=0.4, zorder=12)

    # Path to the county and road shapefiles
    county_shapefile = 'ne_10m_admin_2_counties.shp'
    road_shapefile = 'ne_10m_roads.shp'
    counties = ShapelyFeature(Reader(county_shapefile).geometries(),
                            ccrs.PlateCarree(), edgecolor='brown', facecolor='none', linewidth=0.3)
    roads = ShapelyFeature(Reader(road_shapefile).geometries(), ccrs.PlateCarree(), edgecolor='red', facecolor='none', linewidth=0.5)

    ax.add_feature(roads, zorder=10)
    ax.add_feature(counties, zorder=10)

    meshes = []
    for ds_name in cat.datasets:
        data = cat.datasets[ds_name].remote_access()

        sweep = 0
        rng = data.variables['distanceR_HI'][:]
        az = data.variables['azimuthR_HI'][sweep]
        ref_var = data.variables['Reflectivity_HI']
        ref = raw_to_masked_float(ref_var, ref_var[sweep])
        x, y = polar_to_cartesian(az, rng)

        # Plot data
        mesh = ax.pcolormesh(x, y, ref, cmap=ref_cmap, norm=ref_norm, zorder=15)
        text = ax.text(0.7, 0.02, data.time_coverage_start, transform=ax.transAxes, fontdict={'size': 16})

        meshes.append((mesh, text))

    anim = ArtistAnimation(fig, meshes, interval=500, blit=True)
    
    # Save animation as an HTML5 video
    anim.save("animation.gif", writer="pillow")
    plt.close(fig)