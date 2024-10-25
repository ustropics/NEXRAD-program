from utils import *

from siphon.radarserver import RadarServer
from datetime import datetime, timedelta, time
from matplotlib.animation import ArtistAnimation

import matplotlib
import metpy.plots as mpplots
import cartopy.feature as cfeature
import matplotlib.pyplot as plt

def create_plot():
    dt1 = datetime(2016, 6, 8, 18)

    # Load in radar data and variables
    rs = RadarServer('http://tds-nexrad.scigw.unidata.ucar.edu/thredds/radarServer/nexrad/level2/S3/') # Access THREDDS for data files
    query = rs.query() # Query the server
    dt2 = dt1 # Set specificed time and date
    query.lonlat_point(-82.81, 27.597).time_range(dt2, dt2 + timedelta(hours=1))
    ref_norm, ref_cmap = mpplots.ctables.registry.get_with_steps('NWSReflectivity', 5, 5)

    cat = rs.get_catalog(query)
    cat.datasets

    ds = cat.datasets[0]
    data = ds.remote_access()
    fig = plt.figure(figsize=(10, 7.5))
    ax = new_map(fig, data.StationLongitude, data.StationLatitude)


    # Set limits in lat/lon space
    ax.set_extent([-85.5, -79, 25, 30.11])

    ax.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '50m',edgecolor='face', facecolor='#020514'))
    ax.add_feature(cfeature.NaturalEarthFeature('physical', 'ocean', '50m',edgecolor='face', facecolor='#bbcfda'))
    ax.add_feature(cfeature.LAKES, facecolor='blue', edgecolor='white', alpha=0, zorder=12)
    ax.add_feature(cfeature.STATES.with_scale('50m'), edgecolor='white', linewidth=0.2, zorder=11)
    ax.add_feature(cfeature.BORDERS.with_scale('50m'), edgecolor='white', linewidth=0.4, zorder=11)
    ax.add_feature(cfeature.COASTLINE.with_scale('50m'), edgecolor='white', linewidth=0.4, zorder=12)

    meshes = []
    for ds_name in cat.datasets:
        # After looping over the list of sorted datasets, pull the actual Dataset object out
        # of our list of items and access over CDMRemote
        data = cat.datasets[ds_name].remote_access()

        # Pull out the data of interest
        sweep = 0
        rng = data.variables['distanceR_HI'][:]
        az = data.variables['azimuthR_HI'][sweep]
        ref_var = data.variables['Reflectivity_HI']

        # Convert data to float and coordinates to Cartesian
        ref = raw_to_masked_float(ref_var, ref_var[sweep])
        x, y = polar_to_cartesian(az, rng)

        # Plot the data and the timestamp
        mesh = ax.pcolormesh(x, y, ref, cmap=ref_cmap, norm=ref_norm, zorder=15)
        text = ax.text(0.7, 0.02, data.time_coverage_start, transform=ax.transAxes,
                    fontdict={'size':16})

        # Collect the things we've plotted so we can animate
        meshes.append((mesh, text))

    matplotlib.rcParams['animation.html'] = 'html5'
    ArtistAnimation(fig, meshes)
