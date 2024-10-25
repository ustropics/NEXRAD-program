import ipywidgets as widgets
import datetime as dt

from ipywidgets import Layout

def create_widgets():
    # Time dropdown options
    time_list = [(dt.time(hour=hour, minute=minute)).strftime("%H:%M")
                 for hour in range(24) for minute in range(0, 60, 5)]
    
    label1 = widgets.Label(value='Select the start and end date/time for the radar loop:')
    label2 = widgets.Label(value='Set the latitude and longitude extent for the map output:')
    label3 = widgets.Label(value='Set the latitude and longitude center position for the radar:')
    
    # Start date and time widgets
    widget_start_date = widgets.DatePicker(layout={'width': 'initial'}, description='Start Date/Time', disabled=False, value=dt.date.today())
    widget_start_time = widgets.Dropdown(layout={'width': 'initial'}, options=time_list)
    
    # End date and time widgets
    widget_end_date = widgets.DatePicker(layout={'width': 'initial'}, description='End Date/Time', disabled=False, value=dt.date.today())
    widget_end_time = widgets.Dropdown(layout={'width': 'initial'}, options=time_list)
    
    # Latitude and longitude widgets
    lon1 = widgets.FloatText(value=-85.5, description='Longitudes:', disabled=False, layout=Layout(width='150px'))
    lon2 = widgets.FloatText(value=-79, disabled=False, layout=Layout(width='60px'))
    lat1 = widgets.FloatText(value=25, description='Latitudes:', disabled=False, layout=Layout(width='150px'))
    lat2 = widgets.FloatText(value=30.2, disabled=False, layout=Layout(width='60px'))

    lon3 = widgets.FloatText(value=-82.8, description='Longitude:', disabled=False, layout=Layout(width='150px'))
    lat3 = widgets.FloatText(value=27.6, description='Latitude:', disabled=False, layout=Layout(width='150px'))
    
    
    # Organize the widgets into layouts
    start = widgets.HBox([widget_start_date, widget_start_time], layout=Layout(justify_content='flex-start'))
    end = widgets.HBox([widget_end_date, widget_end_time], layout=Layout(justify_content='flex-start'))
    lon_box = widgets.HBox([lon1, lon2], layout=Layout(justify_content='flex-start'))
    lat_box = widgets.HBox([lat1, lat2], layout=Layout(justify_content='flex-start'))
    
    # Return the complete widget box layout
    return widgets.VBox([label1, start, end, label2, lon_box, lat_box, label3, lon3, lat3], layout=Layout(justify_content='flex-start'))