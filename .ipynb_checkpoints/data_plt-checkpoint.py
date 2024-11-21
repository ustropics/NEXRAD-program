from utils import *
from siphon.radarserver import RadarServer
from datetime import datetime, timedelta
import cartopy.feature as cfeature
from IPython.display import HTML
import metpy.plots as mpplots
import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation, PillowWriter
import os

def process_dataset(ax, ds_name, cat, ref_norm, ref_cmap):
    """Process a single dataset and return the mesh and text."""
    data = cat.datasets[ds_name].remote_access()
    sweep = 0
    rng = data.variables['distanceR_HI'][:]
    az = data.variables['azimuthR_HI'][sweep]
    ref_var = data.variables['Reflectivity_HI']
    ref = raw_to_masked_float(ref_var, ref_var[sweep])

    # Convert polar to Cartesian grid
    x, y = polar_to_cartesian(az, rng)
    extent = [x.min(), x.max(), y.min(), y.max()]

    # Create the image
    mesh = ax.imshow(
        ref, extent=extent, cmap=ref_cmap, norm=ref_norm,
        origin='lower', interpolation='none', zorder=15
    )
    text = ax.text(0.7, 0.02, data.time_coverage_start, 
                   transform=ax.transAxes, fontdict={'size': 16})
    return mesh, text

def create_individual_images(widget_box, save_path="frames"):
    """Create and save individual frames as images."""
    dt1, dt2, lon_1, lon_2, lon_3, lat_1, lat_2, lat_3 = widget_values(widget_box)
    if dt1 == dt2:
        dt2 = dt1 + timedelta(minutes=30)

    # Radar data and variables
    rs = RadarServer('http://tds-nexrad.scigw.unidata.ucar.edu/thredds/radarServer/nexrad/level2/S3/')
    query = rs.query()
    query.lonlat_point(lon_3, lat_3).time_range(dt1, dt2)
    ref_norm, ref_cmap = mpplots.ctables.registry.get_with_steps('NWSReflectivity', 5, 5)
    cat = rs.get_catalog(query)

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # Plot setup
    fig = plt.figure(figsize=(10, 7.5))
    ax = new_map(fig, cat.datasets[0].remote_access().StationLongitude,
                 cat.datasets[0].remote_access().StationLatitude)
    ax.set_extent([lon_1, lon_2, lat_1, lat_2])

    # Add map features
    ax.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '50m', edgecolor='face', facecolor='#020514'))
    ax.add_feature(cfeature.NaturalEarthFeature('physical', 'ocean', '50m', edgecolor='face', facecolor='#bbcfda'))
    ax.add_feature(cfeature.LAKES, facecolor='blue', edgecolor='white', alpha=0, zorder=12)
    ax.add_feature(cfeature.STATES.with_scale('50m'), edgecolor='white', linewidth=0.2, zorder=11)
    ax.add_feature(cfeature.BORDERS.with_scale('50m'), edgecolor='white', linewidth=0.4, zorder=11)
    ax.add_feature(cfeature.COASTLINE.with_scale('50m'), edgecolor='white', linewidth=0.4, zorder=12)

    for i, ds_name in enumerate(cat.datasets):
        mesh, text = process_dataset(ax, ds_name, cat, ref_norm, ref_cmap)
        plt.savefig(f"{save_path}/frame_{i}.png")
        mesh.remove()
        text.remove()
    plt.close(fig)

def create_animation(widget_box, save_path="animation.gif", frames_path="frames"):
    """Create an animation from individual frames."""
    dt1, dt2, lon_1, lon_2, lon_3, lat_1, lat_2, lat_3 = widget_values(widget_box)
    if dt1 == dt2:
        dt2 = dt1 + timedelta(minutes=30)

    # Radar data and variables
    rs = RadarServer('http://tds-nexrad.scigw.unidata.ucar.edu/thredds/radarServer/nexrad/level2/S3/')
    query = rs.query()
    query.lonlat_point(lon_3, lat_3).time_range(dt1, dt2)
    ref_norm, ref_cmap = mpplots.ctables.registry.get_with_steps('NWSReflectivity', 5, 5)
    cat = rs.get_catalog(query)

    # Plot setup
    fig = plt.figure(figsize=(10, 7.5))
    ax = new_map(fig, cat.datasets[0].remote_access().StationLongitude,
                 cat.datasets[0].remote_access().StationLatitude)
    ax.set_extent([lon_1, lon_2, lat_1, lat_2])

    meshes = []
    for ds_name in cat.datasets:
        mesh, text = process_dataset(ax, ds_name, cat, ref_norm, ref_cmap)
        meshes.append((mesh, text))

    anim = ArtistAnimation(fig, meshes, interval=200, blit=True)
    anim.save(save_path, writer="pillow", fps=5)
    plt.close(fig)