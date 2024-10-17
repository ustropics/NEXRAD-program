import cartopy.crs as ccrs
import cartopy.feature as cfeature
import datetime as dt
import ipywidgets as widgets
import matplotlib
import matplotlib.pyplot as plt
import metpy.plots as mpplots
import numpy as np
import sys

from datetime import datetime, timedelta
from ipywidgets import interact, interactive, fixed, interact_manual, Label
from matplotlib.animation import ArtistAnimation
from siphon.radarserver import RadarServer