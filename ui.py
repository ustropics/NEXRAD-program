from imports import *

def create_widgets():
    # Create a list of times from 00:00 to 23:55 in 5-minute intervals
    time_list = [(dt.time(hour=hour, minute=minute)).strftime("%H:%M")
                 for hour in range(24) for minute in range(0, 60, 5)]

    # Create widget elements for date and time selection
    widget_start_date = widgets.DatePicker(layout={'width': 'initial'}, description='Start Date/Time', disabled=False)
    widget_start_time = widgets.Dropdown(layout={'width': 'initial'}, options=time_list)

    widget_end_date = widgets.DatePicker(layout={'width': 'initial'}, description='End Date/Time', disabled=False)
    widget_end_time = widgets.Dropdown(layout={'width': 'initial'}, options=time_list)

    # Create widgets for longitude and latitude
    lon1 = widgets.FloatText(value=7.5, description='Longitude 1:', disabled=False)
    lon2 = widgets.FloatText(value=7.5, description='Longitude 2:', disabled=False)
    lat1 = widgets.FloatText(value=7.5, description='Latitude 1:', disabled=False)
    lat2 = widgets.FloatText(value=7.5, description='Latitude 2:', disabled=False)

    # Arrange the start and end date/time widgets in horizontal boxes
    start = widgets.HBox([widget_start_date, widget_start_time])
    end = widgets.HBox([widget_end_date, widget_end_time])

    # Return the widgets as a vertical box
    return widgets.VBox([start, end, lon1, lon2, lat1, lat2])