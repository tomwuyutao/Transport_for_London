import requests
import geopy.distance
import pandas as pd

list_of_locations = [['longitude', 'latitude', 'duration', 'distance', 'index', 'color']] # Initialize a list to store location data with headers for each attribute.
base_row = [51.5134, -0.0890, 0, 0, 0, '0.1,0.8,0'] # Define a base location row with predefined values.
list_of_locations.append(base_row) # Add the base location to the list of locations.

# Define a function to fetch and return the journey duration from a given URL.
def get_duration(url):
    reply = requests.get(url)
    data = reply.json() # Parse the JSON response into a Python dictionary.
    try:
        duration = (data["journeys"][0]["duration"]) # Extract duration from the first journey.
    except ValueError:
        duration = 1000 # Default duration value in case of error.
    return duration

# Define a function to calculate and return an index based on location, base location, and duration.
def get_index(location, base_location, duration):
    distance = geopy.distance.geodesic(location, base_location).km # Calculate geodesic distance.
    index = duration / distance # Calculate index as duration per kilometer.
    return(index)

# Define a function to determine the color based on the index value.
def get_color_from_index(index):
    RGB_value = '1, 0.98, 0.98' # Default RGB color value.
    if index < 2.5:
        RGB_value = '1,0,0'
    for i in range (25): # Iterate to assign colors based on index ranges.
        lower_bound = 2.5 + 0.15 * i 
        upper_bound = 2.5 + 0.15 * (i + 1)
        if lower_bound < index < upper_bound:
            g_and_b_value = (10 * i) / 255
            RGB_value = '1, ' + str(g_and_b_value) + ',' + str(g_and_b_value)
        i += 1
    return(RGB_value)


base_location = [51.5134, -0.0890] # Set the base location coordinates.
current_location = [0,0] # Initialize current location as a placeholder.
error_list = [['longitude', 'latitude']]  # Prepare a list to record locations that result in errors.

# Loop through a grid of points around the base location.
for x in range(20): # Iterate over latitude adjustments.
    for y in range(40):   # Iterate over longitude adjustments.
        # Calculate current location coordinates based on iteration and offset.
        current_location[0] = base_location[0] - 0.02 * 10 + 0.02 * (x+1)
        current_location[1] = base_location[1] - 0.02 * 20 + 0.02 * (y+1)
         # Construct the API URL with current location coordinates.
        current_url = "https://api.tfl.gov.uk/journey/journeyresults/" + str(current_location[0]) + "," + str(current_location[1]) + "/to/51.5134,-0.0890?20240303?app_id={{app_id}}&app_key="
        
        current_row = [current_location[0], current_location[1]]
        try:
            duration = get_duration(current_url) # Attempt to fetch the duration from the API.
        except KeyError:
            current_row.extend([0, 0, 0, '0,0,0']) # Set the colour for error points to black
            list_of_locations.append(current_row)
            error_list.append(current_row) # Log the problematic location and skip further processing.
            continue
        except ValueError:
            current_row.extend([0, 0, 0, '0,0,0'])
            list_of_locations.append(current_row)
            error_list.append(current_row)
            continue
        
        try:
            # Calculate the index and distance for the current location.
            index = get_index(current_location, base_location, duration)
            distance = geopy.distance.geodesic(current_location, base_location).km
            color = get_color_from_index(index) # Determine the color based on the calculated index.
        except ZeroDivisionError: # Handle division by zero if distance is zero.
            color = '1,0,1' # Color for the base location 
        
        # Append calculated values to the temporary list and add it to the main list.
        current_row.extend([duration, distance, index, color])
        list_of_locations.append(current_row)
        print(current_row)

df = pd.DataFrame(list_of_locations) # Convert the list of location data into a pandas DataFrame for easier manipulation and analysis.
df.to_csv('data/locations.csv', index=False, header = None) # Save the DataFrame to a CSV file named 'locations.csv' in the 'data' directory.

df = pd.DataFrame(error_list) 
df.to_csv('data/errors.csv', index=False, header = None) # Save the error data to a CSV file named 'errors.csv' in the 'data' directory.     
        
time_of_day = [['longitude', 'latitude', 'duration', 'distance', 'index', 'color']] # Initialize a list to store data with a focus on analysis by time of day. 
base_row = [51.5134, -0.0890, 0, 0, 0, '0.1,0.8,0'] # Define a base row with initial values, including coordinates for a specific location (presumably in London),
time_of_day.append(base_row) # Append the base row to the 'time_of_day' list, setting up the initial state for further data additions.

base_location = [51.5134, -0.0890] # Set the base location coordinates for comparison.
current_location = [0,0] # Initialize the current location with a placeholder value.
y = 1 # Initialize the variable 'y' for use in the loop. Note: this is overwritten by the loop.

# Nested loop to iterate through a grid of points around the base location.
for x in range(10): # Loop over a predefined range in the x-direction.
    for y in range(20): # Loop over a predefined range in the y-direction.
        # Calculate the current location's coordinates based on the loop counters.
        current_location[0] = base_location[0] - 0.04 * 5 + 0.04 * (x+1)
        current_location[1] = base_location[1] - 0.04 * 10 + 0.04 * (y+1)
        
        # Construct the API URL for fetching data for the current location.
        current_url = "https://api.tfl.gov.uk/journey/journeyresults/" + str(current_location[0]) + "," + str(current_location[1]) + "/to/51.5134,-0.0890?app_id={{app_id}}&app_key="
        
        current_row = [current_location[0], current_location[1]]
        
        try:
            duration = get_duration(current_url) # Attempt to fetch the journey duration for the current location.
        except KeyError:
            y = 1
            continue
        except ValueError:
            y = 1 # Reset 'y' if a KeyError occurs and continue to the next iteration.
            continue
        try:
            # Calculate the index and distance using the current location, base location, and duration.
            index = get_index(current_location, base_location, duration)
            distance = geopy.distance.geodesic(current_location, base_location).km
            color = get_color_from_index(index) # Determine the color representation based on the calculated index.
        except ZeroDivisionError:
            color = '1,0,1' # Assign a default color in case of division by zero (i.e., when the current location is the base location).
        
        current_row.extend([duration, distance, index, color])
        time_of_day.append(current_row)

df = pd.DataFrame(time_of_day)
df.to_csv('data/time_of_day.csv', index=False, header = None)



tube = [['longitude', 'latitude', 'duration', 'distance', 'index', 'color']] # Initialize a list to store data related to tube travel.
base_row = [51.5134, -0.0890, 0, 0, 0, '0.1,0.8,0'] # Define a base row with default values. This includes the coordinates of a reference point (possibly a central location in London).
tube.append(base_row) # Append the base row to the 'tube' list. This action adds the first set of concrete data to the structure.

base_location = [51.5134, -0.0890] # Define the base location's coordinates.
current_location = [0,0] # Initialize current location coordinates.
y = 1 # Initialize the variable 'y' (though it's immediately overwritten by the loop).

# Double loop to iterate through a grid of points around the base location.
for x in range(20):
    for y in range(40):   
        
        # Calculate the current location's coordinates based on offsets from the base location.
        current_location[0] = base_location[0] - 0.02 * 10 + 0.02 * (x+1)
        current_location[1] = base_location[1] - 0.02 * 20 + 0.02 * (y+1)
        
        # Construct the URL for the TFL API request, specifying 'tube' as the mode of transport.
        current_url = "https://api.tfl.gov.uk/journey/journeyresults/" + str(current_location[0]) + "," + str(current_location[1]) + "/to/51.5134,-0.0890?mode=tube&20240303?app_id={{app_id}}&app_key="
        
        current_row = [current_location[0], current_location[1]]
        
        try:
            duration = get_duration(current_url) # Attempt to get the journey duration from the API.
        except KeyError:
            y = 1 # Skip to the next iteration if a KeyError occurs, resetting 'y' has no effect in this context.
            continue
        except ValueError:
            y = 1 # Skip to the next iteration if a ValueError occurs.
            continue
        
        try:
            # Calculate the index and distance for the current location.
            index = get_index(current_location, base_location, duration)
            distance = geopy.distance.geodesic(current_location, base_location).km
            color = get_color_from_index(index) # Determine the color based on the calculated index.
        except ZeroDivisionError:
            color = '1,0,1' # Color for the base location 
        
        # Append the calculated metrics to the list 'a' and add it to the 'tube' list.
        current_row.extend([duration, distance, index, color])
        tube.append(current_row)
        
df = pd.DataFrame(tube)
df.to_csv('data/tube.csv', index=False, header = None)

buses = [['longitude', 'latitude', 'duration', 'distance', 'index', 'color']] # Initialize a list to store bus journey data, including longitude, latitude, duration, distance, index, and color.
base_row = [51.5134, -0.0890, 0, 0, 0, '0.1,0.8,0'] # Set up a base row with predefined values for a reference location.
buses.append(base_row)

base_location = [51.5134, -0.0890] # Define the base location's coordinates.
current_location = [0,0] # Initialize the current location with placeholder values.
y = 1
# Nested loops to iterate through a grid of points around the base location.
for x in range(20):
    for y in range(40):   
        # Calculate the current location's coordinates based on the loop counters and offsets.
        current_location[0] = base_location[0] - 0.02 * 10 + 0.02 * (x+1)
        current_location[1] = base_location[1] - 0.02 * 20 + 0.02 * (y+1)
        
        # Construct the URL for the TFL API, specifying 'bus' as the mode and including the current coordinates.
        current_url = "https://api.tfl.gov.uk/journey/journeyresults/" + str(current_location[0]) + "," + str(current_location[1]) + "/to/51.5134,-0.0890?mode=bus&20240303?app_id={{app_id}}&app_key="
        
        current_row = [current_location[0], current_location[1]]
        
        try:
            duration = get_duration(current_url) # Attempt to fetch the journey duration via the API.
        except KeyError:
            y = 1
            continue
        except ValueError:
            y = 1
            continue
        
        try:
            # Calculate the index and distance for the current location using predefined functions.
            index = get_index(current_location, base_location, duration) 
            distance = geopy.distance.geodesic(current_location, base_location).km
            color = get_color_from_index(index) # Determine the color based on the efficiency index.
        except ZeroDivisionError:
            color = '1,0,1' # Assign a fallback color in case of division by zero, indicating the base location itself.
        
        # Append the calculated metrics to 'a' and then add 'a' to the 'buses' list.
        current_row.extend([duration, distance, index, color])
        buses.append(current_row)
        
# Saving Bus Data to CSV
df = pd.DataFrame(buses)
df.to_csv('data/buses.csv', index=False, header = None)

