import ipywidgets as widgets
import datetime as dt

from ipywidgets import Layout

def create_widgets():
    # Time dropdown options
    time_list = [(dt.time(hour=hour, minute=minute)).strftime("%H:%M")
                 for hour in range(24) for minute in range(0, 60, 5)]
    
    label1 = widgets.Label(value='Select the start and end date/time for the radar loop:')
    label2 = widgets.Label(value='Select the latitude and longitude extent for the radar loop:')
    
    # Start date and time widgets
    widget_start_date = widgets.DatePicker(layout={'width': 'initial'}, description='Start Date/Time', disabled=False, value=dt.date.today())
    widget_start_time = widgets.Dropdown(layout={'width': 'initial'}, options=time_list)
    
    # End date and time widgets
    widget_end_date = widgets.DatePicker(layout={'width': 'initial'}, description='End Date/Time', disabled=False, value=dt.date.today())
    widget_end_time = widgets.Dropdown(layout={'width': 'initial'}, options=time_list)
    
    # Latitude and longitude widgets
    lon1 = widgets.FloatText(value=7.5, description='Longitudes:', disabled=False, layout=Layout(width='140px'))
    lon2 = widgets.FloatText(value=7.5, disabled=False, layout=Layout(width='50px'))
    lat1 = widgets.FloatText(value=7.5, description='Latitudes:', disabled=False, layout=Layout(width='140px'))
    lat2 = widgets.FloatText(value=7.5, disabled=False, layout=Layout(width='50px'))
    
    # Organize the widgets into layouts
    start = widgets.HBox([widget_start_date, widget_start_time])
    end = widgets.HBox([widget_end_date, widget_end_time])
    lon_box = widgets.HBox([lon1, lon2])
    lat_box = widgets.HBox([lat1, lat2])
    
    # Return the complete widget box layout
    return widgets.VBox([label1, start, end, lon_box, lat_box])