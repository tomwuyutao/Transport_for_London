# Analyzing the Efficiency of London's Public Transport

### 1. Introduction
Our project investigates the effectiveness of London's Transport for London (TfL) network, aiming to identify disparities and improve efficiency across the city. We focus on connectivity to Central London, access to major destinations, comparison of tube and bus services, daily travel time fluctuations, and the link between station traffic and connectivity. By analyzing journey efficiency—measured as time spent per kilometer—we seek actionable insights to enhance London's public transport system.

### 2. Data source
- TfL Journey Planner API 
- TfL Open Data

### 3. Installation
Required Python libraries:
```bash
pip install requests pandas scrapy numpy shapely geopandas geopy plotnine
```

### 4. Running the Code

To process and visualize the data, follow these steps:
1. **Donwload Raw Data**: Ensure the codes run in the directory that contians folders `raw_data` and `London-wards-2018`.

2. **Data Processing**: Clean and prepare the data by running the `data_processing_auto.py` script. This will also organize the output into specific directories. Make sure you are in the directory containing the `task_code` folder before executing the command. This script will delete the existing `data` folder in your directory.

3. **Visualization**: Generate the visualisations for analysing London's public transport by running the cells within `visualisation.ipynb`.

Note that most APIs require user credentials to use. We didn't include any credentials in our code, because TfL's Unified API allows for 50 anonymous requests per minute. This is totally enough for our use case, since the Journey Planner API can at most generate around 30 responses per minute.

An alternative method to run our code is through the jupyter notebook named "Backup method". This is a single jupyter notebook file containing all the code.

### 5. Results and Insights (In Brief)
- TfL network offers strong connectivity to Central London and key destinations.
- Tube system is efficient in west and parts of east London, but less so in the southeast.
- Buses cover wider areas, with travel times only 25% slower than the tube, contradicting Journey Planner estimates.
- Connectivity to Central London is high across both busy and quieter stations, with no clear correlation between station traffic and connectivity.

(This readme file only provides an overview of our project, as more details are discussed in the webpage.)

*This project is powered by TfL Open Data.*

*This project contains OS data © Crown copyright and database rights 2016 and Geomni UK Map data © and database rights 2019.*

