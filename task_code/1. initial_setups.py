# This code sets up the initial working condition for the rest of the codes.
# The function of this code is to ensure that necessary libraries are imported, and there is an empty trojectory "traffic_data" inside the folder 'data'

# Import all necessary libraries for HTTP requests, JSON parsing, data manipulation and analysis, web scraping, geospatial analysis, and creating visualizations.

import json
import pandas as pd
from scrapy import Selector
from scrapy.http import HtmlResponse
import numpy as np
import math
from shapely.geometry import Point
import geopandas as gpd
from geopandas import GeoDataFrame
import geopy.distance
from plotnine import ggplot, aes, geom_point, theme_minimal, labs, scale_x_continuous, scale_y_continuous

#Clean and create initial folders
import shutil
import os

if os.path.exists('data'):
    shutil.rmtree('data')


Data_folder = os.path.join(os.getcwd(), 'data') #This is to create a folder to store data
if os.path.exists(Data_folder) == False:
    os.mkdir(Data_folder)

Traffic_data_folder = os.path.join(Data_folder, 'traffic_data')  # Define the path for the 'traffic_data' folder.
if not os.path.exists(Traffic_data_folder):  # Check if the 'traffic_data' folder doesn't exist.
    os.mkdir(Traffic_data_folder)  # Create the 'traffic_data' folder.
    

