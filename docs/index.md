# Analysing the Efficiency of London's Public Transport

### Table of contents

- Introduction
- Procedure Roadmap
- Data Collection
	- TfL Journey Planner API
	- TfL Open Data
	- Data Collection Challenges
- Data cleaning and processing
	- Journey Planner data
	- Station traffic data
- Visualisation
	- Transport Efficiency
		- Which points cannot be inputted into the Journey Planner?
	- Transport Efficiency (different target locations)
	- Transport Efficiency (tube only)
	- Transport Efficiency (bus only)
	- Transport Efficiency (different times of day)
	- Station Traffic Analysis
- Conclusion
	- Limitations of this study
- Acknowledgments

# Introduction

The London Underground is known for its historical significance and it is recognised as a symbol of London. London also has one of the largest network of underground stations and buses in the world. Yet, a question remains: does this renowned and historic public transit system truly meet the  needs of London's commuters? In our research, we conduct a comprehensive analysis of the TfL network using diverse methodologies. This study not only highlights the system's capabilities and areas for improvement but also seeks to provide a detailed evaluation of its effectiveness within the urban environment. 

After analysing the available data provided by TfL, we decided to break the project down into 5 questions, each of which corresponds to a part in the "Visualisation" section.
- How well are different areas of London connected to Central London?
- How well are different areas of London connected to other popular destinations in London?
- How well do the tube network and the bus network serve different parts of London?
- Does travel time to Central London fluctuate throughout the day?
- Is there a correlation between station traffic and connectivity to Central London?

In this project, we define "connectivity" between two places as the "efficiency" of the journey between them. Additionally, "efficiency" is defined as "time spent per kilometre". The less time spent for every kilometre travel, the more efficient a journey is.

# Procedure Roadmap

<img src="./assets/Untitled 1.png">

# Data Collection

## TfL Journey Planner API

To investigate the connectivity between different areas of London and Central London, we first need to determine the time required to travel from various locations across London to Central London. For most parts of this project, Central London is defined as the Bank Junction[^1], as it is a popular destination for commuters. Note that this project includes [a specific section](#transport-efficiency-different-target-locations) dedicated to investigating Transport Efficiency for destinations other than bank. The destination is referred to as the "target location" in this report

We used the [TfL Journey Planner API](https://api.tfl.gov.uk/swagger/ui/index.html?url=/swagger/docs/v1#!/Journey/Journey_JourneyResults) to find the route to Bank from all around London. The structure of the API is illustrated below:

<img src="./assets/API breakdown.png">

The Journey Planner API is used in five different analyses:
-  Transport efficiency when utilizing all modes of public transport.
-  Difference in transport efficiency between several popular destinations.
-  Efficiency of London buses.
-  Efficiency of London Underground.
-  Efficiency at different times of the day.

To obtain all the data points, we performed some calculations based on the geography of London and identified a starting point at the lower-left corner of London. The loop then increments *x* by 0.02 (approximately 2 km) twenty times and *y* by 0.02 forty times, resulting in a total of 800 [^2] data points required. For every point, the coordinate data is send to the Journey Planner API to get the duration of journey from that point to Bank.The process is depicted below:

<p align="center">
  <img src="./assets/Data collection process.png" width="500">
</p>

## TfL Open Data

To collect station traffic and location data, we used the [TfL Open Data](https://tfl.gov.uk/info-for/open-data-users/our-open-data?intcmp=3671) page. Our dataset spans from 2017 to 2022. This phase of data acquisition was a straightforward process; we downloaded the necessary CSV files from the TfL page. Subsequently, we carefully cleaned the traffic data and merged it with station location data for mapping purposes.

## Data Collection Challenges

During the data collection process, we encountered four significant challenges:

1. **Slow response from Journey Planner API**: One major hurdle was the slow response time from the Journey Planner API. To illustrate, running the program on 3200 different locations could take over 10 hours, and it occasionally crashes midway. To address this, we reduced the number of locations processed and utilised Google Cloud computing to assist in our calculations.
2. **Disruptions due to strikes and station closures**: Unforeseeable events like strikes and station closures posed a potential impact on the analysis of transport efficiency. Fortunately, we identified a workaround within the API that allowed us to plan journeys at future times, thereby enhancing the accuracy of our results.
3. **The downloaded data has different structures**: Station traffic data collected prior to 2017 exhibited a vastly different CSV structure compared to more recent data. A lot of cleaning is needed before merging these files together.
4. **Limited API documentation**: TfL's API documentation lacked detailed information, offering only generic explanations that did not include the various parameters used in the Journey Planner API. To overcome this challenge, we scoured the TfL tech forum and Reddit for insights and solutions. We also rely on the Postman package provided by TfL when experimenting with the API.
5. **Journey Planner data has to be generated in real-time**. There is no way to simply download these data and experiment with calculations. Every time we want to test our code, we have to send hundreds of requests and wait for the results. This makes the process of experimenting and debugging very time-consuming.

# Data cleaning and processing

## Journey Planner data

The data retrieved from the TfL Journey Planner API are already very clean to start with. This is primarily because we select the inputs ourselves and provide them to the API, resulting in significantly cleaner data compared to methods such as web scraping or downloading CSV files. 

However, it's worth noting that there are instances where certain locations cannot be used as inputs for the TfL Journey Planner. In other words, the API returns null results for some starting locations (we call these points "error points"). In our code, we still include these data in the dataframe to avoid confusion (this is explained [later](#which-points-cannot-be-inputted-into-the-journey-planner) in greater detail). We also append these error points to a separate [errors.csv](https://github.com/lse-ds105/ds105a-project-name_not_found/blob/fa2445f5f473b2e2341e98cf6cc0605530d6bffa/data/errors.csv) dataframe.

To process the raw data obtained from the TfL Journey Planner API, we first add these metrics to our dataframe:
- **Longitude and Latitude** (float), which represent the coordinates of the journey's starting point.
- **Duration** (int), indicating the total duration of the journey.

Additionally, we used the .apply function of Pandas to compute three more pieces of information:
- **Distance** (float), calculated from the coordinates, measuring the distance between the starting point and the destination.
- **Index** (float), measuring how many minutes it takes to travel one kilometre. A lower index indicates a more efficient journey, calculated as duration/distance.
- **colour** (str in the dataframe, later converted to a tuple for mapping), representing the magnitude of the index [^3]. 

And the results are: [^4]

| longitude | latitude | duration | distance           | index              | colour                                        |
|-----------|----------|----------|--------------------|--------------------|----------------------------------------------|
| 51.5134   | -0.089   | 0        | 0                  | 0                  | "0.1,0.8,0"                                      |
| 51.3334   | -0.469   | 109      | 33.16129631        | 3.2869643872273104 | "1, 0.19607843137254902,0.19607843137254902" |
| 51.3334   | -0.449   | 112      | 32.063491561514084 | 3.4930693616173096 | "1, 0.23529411764705882,0.23529411764705882" |
| 51.3334   | -0.429   | 145      | 30.98925410552983  | 4.679041305938554  | "1, 0.5490196078431373,0.5490196078431373"   |
| 51.3334   | -0.409   | 146      | 29.94112079737464  | 4.876236965        | "1, 0.5882352941176471,0.5882352941176471"   |
| 51.3334   | -0.389   | 159      | 28.921929908443175 | 5.4975584445207835 | "1, 0.7450980392156863,0.7450980392156863"   |

## Station traffic data

The station traffic data we downloaded required thorough cleaning due to two key issues:
- Some stations were constructed after 2016, resulting in missing station traffic data.
- Station names are labelled differently in the files over the years. For instance, Canary Wharf Station was labelled as "Canary Wharf" in the station location file and the 2016 station traffic file, but it was referred to as "Canary Wharf LU" in traffic files from 2017 onwards.

Our cleaning process comprised several steps:
- We initiated the cleaning of the downloaded station traffic data by eliminating zero rows and removing unnecessary columns.
- We developed a function to strip ' LU' from station names to ensure consistency.
- We aggregated traffic data from all years into a single dataframe to compute the average traffic.
- Based on the average traffic, we assigned a colour value to each station[^5].
- We merged the average traffic data with the station location data.
- We retained rows with missing data for the sake of completeness, but these rows would be disregarded during the visualisation phase.

The final dataframe includes the following fields:
- **Station** (str): Denoting the station name.
- **2016-2022** (int): Representing the raw station traffic data obtained from TfL Open Data.
- **Average_traffic** (float): Calculated as the average of traffic data from 2017 to 2022 (we decided to drop the year 2016, which is explained here [^6]).
- **Colours** (str in the dataframe, later converted to a tuple for mapping): Indicating the magnitude of the average traffic. 

| |Station     |2016    |2017    |2018    |2019    |2020   |2021   |2022    |Average_traffic   |Colours                                 |X           |Y          |
|------|------------|--------|--------|--------|--------|-------|-------|--------|------------------|---------------------------------------|------------|-----------|
|0     |Acton Town  |6274649 |5731527 |5794685 |6186555 |3568528|2902697|4931972 |4159423.4285714286|0.7227051047619047,0.7227051047619047,1|-0.280251204|51.50274977|
|1     |Aldgate     |8009494 |8459234 |9218140 |9956600 |2775844|3525128|6902494 |5833920           |0.6110720000000001,0.6110720000000001,1|-0.075614184|51.51427182|
|2     |Aldgate East|13434630|13262408|13707738|14148654|3144899|5611130|10229488|8586331           |0.4275779333333334,0.4275779333333334,1|-0.07228712 |51.51523341|
|3     |Alperton    |3174845 |2896391 |2796159 |2858439 |2064990|1345253|2302973 |2037743.5714285714|0.8641504285714285,0.8641504285714285,1|-0.299486539|51.54069477|
|4     |Amersham    |2360700 |2215502 |2130207 |2350099 |863361 |946577 |1657141 |1451841           |0.9032106,0.9032106,1                  |-0.607478839|51.67414971|
|5     |Angel       |20100806|18236123|17661269|17705761|5255371|7258744|12371592|11212694.285714285|0.2524870476190476,0.2524870476190476,1|-0.105789914|51.53249887|
|6     |Archway     |9940993 |8806365 |8608964 |8772643 |4429802|4027456|6798862 |5920584.571428572 |0.6052943619047619,0.6052943619047619,1|-0.135113518|51.56542675|


# Visualisation

## Transport Efficiency

<img src="./assets/Pasted image 20240205221102.png">

Note: The more red a point is, the more efficient (in terms of time spent per kilometre) it is to get from that point to Bank. The green point at the centre is the location of Bank, the target location of this map. The black points are those that cannot be inputted into the journey planner, more on these are explained [later](#which-points-cannot-be-inputted-into-the-journey-planner). In this report we will refer to this graph as the "map for Bank".

In general, TfL does an exceptional job serving London's extensive urban area. The majority of London is marked in red on our visualisation, signifying **a high level of accessibility to Central London from all around the city**. This accessibility extends even to the suburban areas, with very few regions experiencing transport blind spots. Notably, the southeastern sector of London, primarily reliant on London Overground and National Rail services, is the weak part of London's public transport network. 

One might observe that the Central area appears predominantly white, indicating lower efficiency. This is entirely reasonable for short-distance journeys. For example, consider a trip from LSE to Bank. This journey starts with a five-minute walk to the tube station, coupled with additional waiting time for the tube's arrival, significantly affecting Transport Efficiency. Conversely, imagine travelling from Hammersmith to Bank, where a larger proportion of time is spent on the train, resulting in a considerably more efficient journey from a time spent per kilometer perspective.

<p align="center">
  <img src="./assets/Pasted image 20240203213724.png" width="500">
</p>

Note: the scale looks a bit strange here because it aligns with later graphs. This makes comparisons between graphs easier.

In the graph above, we chart the duration of 800 journeys against their travel distance in kilometres. The data reveals a noteworthy trend: **When travelling from locations within a 15-kilometre radius of the Bank, one can almost always anticipate an efficient journey**, typically taking around an hour. However, as the distance exceeds 20 kilometres, there are occasional instances of 'blind spots' where the commute to Bank, for instance, can take more than 200 minutes.

<p align="center">
  <img src="./assets/Pasted image 20240203213734.png" width="500">
</p>

The above plot depicting the relationship between distance and the efficiency index reveals that **London's public transport operates at its highest efficiency when the travel distance falls within the 10-25 kilometre range**. This aligns seamlessly with our expectations, as the typical distance between London's residential boroughs and (Bank) is between 10-25 kilometres [^7]. 

### Which points cannot be inputted into the Journey Planner?

It's essential to note the presence of certain locations that cannot be inputted into the journey planner. These points, while absent on the graph, could be misinterpreted as inefficient ones due to the graph's white background. To prevent this potential confusion, I've changed the colour of these error points to black to clearly distinguish them.

While it is technically possible to travel from these error points to Bank, calculating the precise travel time presents a challenge. The majority of these locations are situated within suburban forests and rivers, rarely visited by individuals. Given their limited number, approximately a dozen in total, we have opted to retain their black colour on the graph, as they do not significantly impact the overall analysis.

Here is a visualisation of the error points specifically:

<p align="center">
	<img src="./assets/Pasted image 20240206194727.png" width="500">
</p>

## Transport Efficiency (different target locations)

Not everyone want to travel to Bank all the time. We decided to include more target locations to better understand how efficient the TfL network is. To get these graphs, we can simply change the base location in our code [^8].

Canary Wharf

<p align="center">
	<img src="./assets/Pasted image 20240206172828.png" width="500">
</p>

What if you study at LSE?

<p align="center">
	<img src="./assets/Pasted image 20240206173002.png" width="500">
</p>

Or you happen to be a student from Imperial?

<p align="center">
	<img src="./assets/Pasted image 20240206172859.png" width="500">
</p>

<img src="./assets/comparison between locations.jpg">

Canary Wharf, LSE, and Imperial College London are situated close to Central London (Bank). Upon analyzing these three locations in comparison to the map for Bank, we observed a consistent pattern among the outer points on the map. The primary difference between them lies in the distribution of white points, which are centred around the initial starting point (the green point).

Furthermore, our analysis suggests that **Holborn and South Kensington enjoy a level of connectivity comparable to that of prominent commuter hubs such as Bank and Canary Wharf**. This underscores the comprehensive coverage provided by TfL (Transport for London) throughout Central London. TfL's commitment extends beyond merely serving business districts, ensuring equitable accessibility to all areas within Central London.

Heathrow Airport

<p align="center">
	<img src="./assets/Pasted image 20240205220850.png" width="510">
</p>

Luton Airport

<p align="center">
	<img src="./assets/Pasted image 20240205233120.png" width="700">
</p>

Gatwick Airport

<p align="center">
	<img src="./assets/Pasted image 20240205233139.png" width="680">
</p>

These airport graphs show a consistent trend: a majority of data points in London are depicted in red. This uniformity implies **a high level of efficiency (in terms of time spent per kilometre) when travelling to airports, regardless of one's location within the city**. Upon delving into the journey planner data, it becomes evident that most airport-bound trips involve utilizing specialized airport express trains, such as the Gatwick Express and Luton Airport Express. These trains significantly enhance the overall journey's efficiency due to their speed.

It is worth noting that the prevalence of red points on these graphs raises a potential limitation in our research methodology when analyzing airport journeys. The sheer amount of red points makes it different to identify meaningful patterns. Therefore, it might be better to redefine an "efficient" journey to and airport by focusing on total time spent as opposed to time spent per kilometre. This adjustment could yield more insightful results for our analysis of airport-related journeys.

## Transport Efficiency (tube only)

<img src="./assets/Pasted image 20240205124548.png">

<img src="./assets/tube map vs original.jpg">

What if you value the punctuality of the tube and hate getting stuck in a traffic jam while on a bus? Upon configuring the Journey Planner API to exclusively consider tube routes, the resulting graph paints a distinct picture. A comparison between this graph and the one for Bank highlights the fact that the tube network does not extend to many areas, including the southeastern and certain northern regions of London. The tube serves West London and select portions of East London especially well. In conclusion, **the tube excels in serving specific locations but is entirely inaccessible to others**.

<p align="center">
  <img src="./assets/Pasted image 20240203213748.png" width="500">
</p>

<img src="./assets/tube scatter vs original.jpg">

We see a similar pattern between distance and duration compared to the graph for Bank. The difference is that the tube-only scatterplot is a lot more scattered, while points in the original scatterplot are more clustered. Therefore we conclude that **holding the distance from Bank constant, tube-only journeys have considerably more variation in their durations**. This finding indicates that while the tube system can be highly efficient in some instances, there are situations where taking a bus to reach the tube station first becomes a necessity.

<p align="center">
  <img src="./assets/Pasted image 20240203213758.png" width="500">
</p>

<img src="./assets/tube scatter 2 vs original.jpg">

The scatterplot between distance and index also has a similar pattern to the scatterplot for Bank. Note that the index has slightly more variation and sometime the journey can be very inefficient. 

## Transport Efficiency (bus only)

<img src="./assets/Pasted image 20240205124558.png">

<img src="./assets/bus map vs original.jpg">

Using the same method as the tube, we produced the map for bus-only journeys. This map exhibits a pattern similar to the original map for Bank, albeit with an overall lower efficiency. In comparison to the tube network, **buses have greater coverage, display less variability among different regions, but achieve a lower maximum efficiency**.

<img src="./assets/tube map vs bus map.jpg">

One intriguing observation emerges when comparing these maps: **the tube-only map and the bus-only map exhibit nearly perfect complementarity**. As shown on the maps above, most white areas in the left map are covered in red in the right one, and vice versa. This indicates that in regions where the tube system proves inefficient, the bus network fills the void; conversely, in areas that the tube serves well, there is a reduced presence of bus service. This observation underscores the meticulous planning of the transportation network, aimed at optimizing efficiency across all areas while minimizing redundancy.

<p align="center">
  <img src="./assets/Pasted image 20240203213810.png" width="500">
</p>

<img src="./assets/bus scatter vs original.jpg">

When compared to the original scatterplot for Bank, the curve for buses is slightly higher than the right curve, indicating that **a journey with only bus typically takes about 1.3x more time**. As seen on the comparison above,  This is a lot better than what we expected, since most of us consider buses as inefficient. If the duration of bus journeys were correctly estimated by the Journey Planner, then the **bus can be a great alternative to the tube for lots of people and should be utilised more**, since it is cheaper and has mobile coverage while being only 30% slower. However, one potential concern is that the Journey Planner may not adequately account for the impact of traffic congestion on bus speed, thereby portraying the bus as more efficient on paper than it might be in practice.

One notable finding is that **the bus excels in short-range travel**. This conclusion is drawn from the striking similarity of the <10 segments in both graphs, meaning that taking a bus for short journeys won't result in significantly longer durations. This finding aligns seamlessly with common intuition.  For instance, when getting from your student hall to LSE, the map often suggests you to take a bus. This is largely because most student halls in Central London are situated within a  5-10 minute walk to the nearest tube station, but typically only a minute away from a nearby bus stop. As considering the journey is only around 20 minutes, the lower walking time can make the bus more efficient compared to the tube.

<p align="center">
  <img src="./assets/Pasted image 20240203213820.png" width="500">
</p>

<img src="./assets/bus scatter 2 vs original.jpg">

Much like the previous findings, the bus network exhibits slower travel times overall. However, **the bus demonstrates less variation in the efficiency index when compared to the tube**. 

## Transport Efficiency (different times of day)

<img src="./assets/Comparison between different times of day 1.png">
Note: we reduced the number of points here to make the process faster

Here is a comparison of the map for bank at 3 different times of day: 9:00, 13:00 and 17:00. Upon careful inspection, we found that there are some differences between these three graphs, but the differences in efficiency are very minor and are hard to notice. 

Additionally, we conducted an experiment using the TfL Go app on our phones, requesting directions from my student hall to Knightsbridge. The results consistently indicated travel times falling within the range of 28 to 32 minutes. It is challenging to pinpoint the precise factors contributing to these differences, but we can reasonably infer that **the timing of a journey may not significantly impact its duration**. It is also possible that the TfL Journey Planner does not account for factors such as station congestion or road traffic congestion in its route calculations.

## Station Traffic Analysis

<img src="./assets/Pasted image 20240206195647.png">
Note: The more blue a point is, the higher its average traffic is between 2017 and 2022 [^9]

Presented here is a visual representation of station traffic data plotted on a map. As anticipated, the majority of stations in Central London experience high traffic volumes. We observe several stations located at a significant distance from Bank, yet still boasting high average traffic. Notable examples include Wembley, Ealing, Wimbledon, Seven Sisters, and Walthamstow Central. These points will be main focus when we compare the traffic data to the original map for Bank.

To determine whether these stations are better served by the TfL network compared to quieter stations, we must compare this data with the earlier map depicting transport efficiency.

<img src="./assets/Pasted image 20240205231436.png">

We see a similar pattern when comparing the traffic data to the map for Canary Wharf:

<img src="./assets/Pasted image 20240205223326.png">

Prior to the start of this project, we expected that the TfL network would provide exemplary service to the popular stations in the suburbs. Our findings agree that the popular stations has easy access to Bank. For instance, consider the blue dot situated in the upper left corner, representing Wembley Station. It is encompassed by a cluster of vibrant red dots, signifying that the commute from Wimbledon to Bank is relatively efficient. 

However, the map reveals that even the quieter stations are well connected to Central London. For example, the large cluster of white points in the upper left corner indicate that these stations experience little traffic, but there too have easy access to Bank. Therefore, **no significant correlation is observed between station traffic and connectivity to Central London**. We infer that when designing the TfL network, TfL wants to have every place in London well connected to Central London, no matter whether it is a busy station ora quiet one. 

One reason that we cannot see a big different in connectivity between busy stations and quiet stations is that our analysis only analysed the efficiency of getting to Bank and canary wharf. When travelling from a station in the suburbs to another station in the suburbs, the busier station might have a bigger advantage since it probably has more underground lines. However, given the slow response of the TfL API, we find it hard extend the coverage of our comparison.

# Conclusion

Here are the key takeaways from our study:
- In general, TfL network serves different parts of London surprisingly well. Regardless of your residence within the city, you can almost always enjoy robust connectivity, not only to Central London but also to popular destinations such as Canary Wharf and Heathrow Airport. 
- Both busier and quieter stations enjoy excellent connections to Central London, with no significant correlation observed between station traffic and connectivity to Central London. 
- While the tube system excels in serving specific areas like west London and certain parts of the east, it remains inaccessible to areas such as south-eastern London. 
- Buses offer broader coverage compared to the tube, and our findings indicate that they are only approximately 30% slower. 
- Results from the Journey Planner shows that the timing of a journey does not significantly impact its duration. However, when we consider this observation in conjunction with the findings in bus speeds, it raises a question about whether TfL's Journey Planner accurately incorporates congestion into its calculations.


### Limitations of this study

There are several considerations to bear in mind. Firstly, it's essential to recognize that **the scope of this study is relatively limited in terms of the number of destinations included**. Evaluating efficiency comprehensively can be challenging with only these few destinations. While we initially considered applying our journey planner algorithm to all available data points, this approach proved impractical due to the slow response time of TfL's API.

Secondly, it's worth noting that **the TfL journey planner has certain limitations**. For instance, it lacks the capability to combine cycling with public transport, despite this often being the fastest mode of travel. The TfL Journey Planner can only accommodate journeys exclusively by bicycle.

Thirdly, even though TfL has made significant efforts in making data accessible to the public, there are still **instances of missing data** that impact our study. For instance, the absence of location data for London Overground and National Rail Stations poses a challenge to our analysis.

Lastly, in this project we define "efficiency" of a journey as time spent per kilometre. However, **time spent per kilometre might not be the perfect metric for how good a journey is**. Say you live 50 kilometres away from Gatwick Airport, and you can get there in 3 hours. This would yield an "index" of 3.6, indicating that on average, 3.6 minutes are spent per kilometre, which is considered pretty efficient in our study. But spending 3 hours on public transport to get to an airport is not a pleasant journey by all means. Some may argue that one can just judge a journey purely based on the duration. We have actually experimented with this approach, but found it hard to identify any patterns since most short journeys are considered "efficient" and longer ones are "inefficient". Although our definition of "efficiency" is not perfect, we think it is the best we can get.

# Acknowledgments

- Tom focused on writing the code and analysing the data.
- Zian took care of getting the data. He used different tools to make sure we got all the right information.
- Allen focused on organising team meetings, preparing the presentation, and building the webpage.

We also want to express our gratitude to Professor Jon Cardoso-Silva and Mr. Mustafa Can Ozkan for their valuable insights and guidance throughout the project. Their expertise and support were instrumental in our project's success.

*This project is powered by TfL Open Data.*

*This project contains OS data © Crown copyright and database rights 2016 and Geomni UK Map data © and database rights 2019.*

[Link to Code Repository](https://github.com/lse-ds105/ds105a-project-name_not_found)

### Footnotes

[^1]: The coordinates of Bank Junction is 51.5134,-0.089, which is included in the first row of the dataframes
[^2]: From our experiences, 800 data points is the perfect balance between accuracy and calculation time. Adding more points can make the calculations too slow.
[^3]: There is a more efficient way to assign different colour values to data points. This can be done directly in the graphing process, eliminating the need for an extra column. However, since our method has been working perfectly, we decided not to make any changes.
[^4]: You may notice that the first row contains a lot of zeros. That is because the first row indicates the destination of the journey (Bank). This is included for mapping purposes.
[^5]: Similarly, there is a better way to assign colour values.
[^6]: Initially, we intended to incorporate data spanning from 2016 to 2022. However, after observing the merged dataframe, we realised that the year 2016 has too much missing data, and it is not worth it to include one more year of data at the cost of missing 20+ stations. So we eventually dropped the year 2016 from the average traffic calculations.
[^7]: For reference, Wembley and Walthamstow are both 15km away from Bank.
[^8]: Since the data collection and visualisation methodology for these locations is identical to the process used for mapping the data related to Bank (as presented in Part 1 of our Visualisation), we have made the decision to exclude the code for these plots from our final code. This modification is intended to prevent the excessive generation of plots within our code, which could make navigation through various sections of our code cumbersome.
[^9]: You may notice the absence of many stations in southeastern London can be attributed to the fact that this part of the city relies primarily on the London Overground and National Rail services. Unfortunately, station location data for London Overground and National Rail stations, such as East Croydon and West Croydon, is unavailable.
