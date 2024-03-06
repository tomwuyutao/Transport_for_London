import pandas as pd

def clean_and_save_csv(file_name, year): # Function to clean the 'en/ex' column and save the CSV file
    # Read the CSV file
    df = pd.read_csv(file_name)
    # Clean 'en/ex' column
    df['en/ex'] = df['en/ex'].astype(str).str.replace(',', '').str.strip()
    df['en/ex'] = pd.to_numeric(df['en/ex'], errors='coerce')   # Convert to numeric, coercing errors to NaN
    df['en/ex'] = df['en/ex'].fillna(0).astype(int)              # Replace NaNs with 0 and convert to int
    selected_columns = ['NLC', 'Station', 'en/ex']
    
    df_filtered = df[selected_columns]
    # Save the cleaned data back to CSV
    cleaned_file_name = f"data/traffic_data/Cleaned_AnnualisedEntryExit_{year}.csv"
    df_filtered.to_csv(cleaned_file_name, index=False)
    
    return cleaned_file_name  # Return the file name of the cleaned file

def get_color_from_average_traffic(average_traffic):
    # 78840000, 280000
    r_and_g_value = 1 - (average_traffic / 20000000)
    if r_and_g_value < 0: 
        r_and_g_value = 0
    # Construct an RGB value string, keeping the blue component constant.
    RGB_value = str(r_and_g_value) + ',' + str(r_and_g_value) + ',1'
    return(RGB_value)

def load_data(year): # Loading and Cleaning Data per Year
    file_path = f'data/traffic_data/Cleaned_AnnualisedEntryExit_{year}.csv'
    df = pd.read_csv(file_path)
    df['en/ex'] = pd.to_numeric(df['en/ex'], errors='coerce')
    df = df.dropna(subset=['en/ex'])
    df.rename(columns={'en/ex': str(year)}, inplace=True)
    df = df.drop_duplicates(subset=['NLC'])
    return df

def clean_station_name(name):
    item = name.replace(' LU','')
    return item

csv_files = [
    'raw_data/AnnualisedEntryExit_2016.csv', 
    'raw_data/AnnualisedEntryExit_2017.csv', 
    'raw_data/AnnualisedEntryExit_2018.csv', 
    'raw_data/AnnualisedEntryExit_2019.csv',
    'raw_data/AC2020_AnnualisedEntryExit.csv',
    'raw_data/AC2021_AnnualisedEntryExit.csv',
    'raw_data/AC2022_AnnualisedEntryExit.csv'
]

x = 2016

for csv_file in csv_files: # Clean and save each CSV file
    try:
        cleaned_file = clean_and_save_csv(csv_file, x)
        print(f"Cleaned file saved to: {cleaned_file}")
        x+=1
    except FileNotFoundError as e:
        print(f"File not found: {csv_file}. Please check the file name and path.")
        
# Load data for each year
dfs = {year: load_data(year) for year in range(2016, 2023)}

# Merge the dataframes while ensuring no duplicate column names
df_station_traffic = None
for year, df in dfs.items():
    if df_station_traffic is None:
        df_station_traffic = df
    else:
        # Before merging, rename overlapping columns except for the 'Station' column
        df['Station'] = df['Station'].apply(clean_station_name)
        df = df.rename(columns={col: f"{col}_{year}" for col in df.columns if col not in ['Station', str(year)]})
        df_station_traffic = pd.merge(df_station_traffic, df, on='Station', how='outer', suffixes=('', f'_{year}'))

# Calculate the average traffic across all years and determine color codes.
df_station_traffic['Average_traffic'] = ((df_station_traffic['2017'] + df_station_traffic['2018'] + df_station_traffic['2019'] + df_station_traffic['2020'] + df_station_traffic['2021'] + df_station_traffic['2022'])) / 7
df_station_traffic['Colors'] = df_station_traffic['Average_traffic'].apply(get_color_from_average_traffic)

# Select and rearrange the columns for the final output DataFrame.
output_columns = ['Station'] + [str(year) for year in range(2016, 2023)] + ['Average_traffic'] + ['Colors']
df_station_traffic_merged = df_station_traffic[output_columns]

station_locations = pd.read_csv('raw_data/station_locations.csv')

# Rename the 'Name' column to 'Station' for consistency with the traffic data.
station_locations = station_locations.rename(columns={'Name': 'Station'})

# Merge the traffic data with station locations on the 'Station' column.
df_station_traffic_merged = df_station_traffic_merged.merge(station_locations, left_on='Station', right_on='Station')

# Save the merged DataFrame to a CSV file for future use.
df_station_traffic_merged.to_csv('data/station_traffic_merged.csv') 


