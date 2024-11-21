import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

from datetime import datetime

def widget_values(widget_box):
    start_date = widget_box.children[1].children[0].value
    start_time = widget_box.children[1].children[1].value

    end_date = widget_box.children[2].children[0].value
    end_time = widget_box.children[2].children[1].value

    start_year = start_date.year
    start_month = start_date.month
    start_day = start_date.day
    start_time = datetime.strptime(start_time, '%H:%M').time()

    end_year = end_date.year
    end_month = end_date.month
    end_day = end_date.day
    end_time = datetime.strptime(end_time, '%H:%M').time()

    dt1 = datetime(start_year, start_month, start_day, start_time.hour, start_time.minute)
    dt2 = datetime(end_year, end_month, end_day, end_time.hour, end_time.minute)

    lon_1 = widget_box.children[4].children[0].value
    lon_2 = widget_box.children[4].children[1].value
    lon_3 = widget_box.children[7].value

    lat_1 = widget_box.children[5].children[0].value
    lat_2 = widget_box.children[5].children[1].value
    lat_3 = widget_box.children[8].value

    return dt1, dt2, lon_1, lon_2, lon_3, lat_1, lat_2, lat_3

# Convert raw data to floating point values
def raw_to_masked_float(var, data):
    data = np.ma.array(data, mask=data==0)
    return data * var.scale_factor + var.add_offset

# Convert from polar to cartesian coordinates for plotting
def polar_to_cartesian(az, rng):
    az_rad = np.deg2rad(az)[:, None]
    x = rng * np.sin(az_rad)
    y = rng * np.cos(az_rad)
    return x, y

# Create projection for map output
def new_map(fig, lon, lat):
    proj = ccrs.LambertConformal(central_longitude=lon, central_latitude=lat)
    ax = fig.add_axes([0.02, 0.02, 0.96, 0.96], projection=proj)
    return ax