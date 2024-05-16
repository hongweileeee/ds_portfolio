# ![](https://ga-dash.s3.amazonaws.com/production/assets/logo-9f88ae6c9c3871690e33280fcf557f33.png) Project 1: Exploring climate data in correlation with domestic electricity consumption in Singapore

### Problem Statement

Global warming has been the cause of increasingly prolonged heat waves in Singapore over the months of April and May, and intensified rainfall extremes over the monsoon months. [(NEA, 2024)](https://www.nea.gov.sg/media/news/news/index/latest-climate-projections-for-singapore-show-intensifying-urban-heat-and-more-wet-dry-extremes.)

Concerns have been raised during parliament [(MTI, 2023)](https://www.mti.gov.sg/Newsroom/Parliamentary-Replies/2023/07/Written-reply-to-to-PQs-on-electricity-demand-and-grid-stress-from-prolonged-heat-wave) on electricity demand and grid stress during these extreme weather conditions in Singapore. While it has been temporarily resolved that our peak capacity is still higher than the peak national demand, there are still expectations on EMA to ensure that we are efficient in catering for local electricity demands, especially during extreme weather periods in the future.

Essentially, how can EMA’s energy supply be better prepared for the increased electricity demand and grid stress from climate fluctuations?

The aim is to provide EMA (Energy Market Authority) with insights in management of electricity generation and distribution based on climate fluctuations.

---

### Data Dictionary

|Feature|Type|Dataset|Description|
|---|---|---|---|
|**year_month**|*object*|Climate data|Date values in 'yyyy-mm' format, from 2018 January (2018-01) to 2022 August (2022-08)| 
|**total_rainfall**|*float*|Climate data|The volume of rainfall (measured in mm) over 2018 to 2022 August|
|**no_of_rainy_days**|*float*|Climate data|The total number of rainy days measured monthly over 2018 to 2022 August. (A day is considered to have “rained” if the total rainfall for that day is 0.2mm or more.)|
|**mean_rh**|*float*|Climate data|Monthly average relative humidity, expressed in percentages, is a ratio of the amount of atmospheric moisture present relative to the amount that would be present if the air were saturated.|
|**mean_sunshine_hrs**|*float*|Climate data|Measured with a pyrheliometer comprising of a glass globe and recorder card. The number of hours of sunshine each day is derived from the time taken between the first and last burnt marks on the card.|
|**mean_temp**|*float*|Climate data|Average monthly temperature, measured with a thermometer in degrees celsius by Singapore's weather stations|
|**wet_bulb_temperature**|*float*|Climate data|Average monthly wet bulb temperature. A composite measure that takes into account air temperature, humidity, wind and solar radiation, and it is different from air temperature.|
|**1rm_cons**|*float*|Singapore Energy Statistics|Average monthly electricity consumption of 1 room and 2 room flats in Singapore. Measured in kWh.|
|**3rm_cons**|*float*|Singapore Energy Statistics|Average monthly electricity consumption of 3 room and 4 room flats in Singapore. Measured in kWh.|
|**5rm_cons**|*float*|Singapore Energy Statistics|Average monthly electricity consumption of 5 room and Executive flats in Singapore. Measured in kWh.|
|**condo_cons**|*float*|Singapore Energy Statistics|Average monthly electricity consumption of Condominiums and Private Apartments in Singapore. Measured in kWh.|
|**landed_cons**|*float*|Singapore Energy Statistics|Average monthly electricity consumption of Private landed properties in Singapore. Measured in kWh.|
|**public_cons**|*float*|Singapore Energy Statistics|Average monthly electricity consumption of all public housing (HDB flats) in Singapore. Measured in kWh.|
|**private_cons**|*float*|Singapore Energy Statistics|Average monthly electricity consumption of all private housing (Condominiums, private apartments and landed properties) in Singapore. Measured in kWh.|

### Summary of Findings

Based on the analysis of 2018 January to 2022 August, we have observed that:
1. Wet bulb temperature and number of rainy days have the strongest correlations with Electricity consumption. A 1°C increase in wet bulb temperature correlates to an increase in electricity consumption of public housing by 39.59kWh and private housing by 44.01kWh, while an extra day of rain correlates with a 40.8kWh increase in electricity consumption across dwelling types. 
2. Household electricity consumption has mildly positive correlations with temperature. An increase in temperature by 1°C correlates to an increase in electricity consumption of public housing by 23.89kWh and private housing by 28.05kWh.
3. There are anomalous situations that has to be taken into account, such as during the COVID pandemic, temperatures dropped slightly however household electricity consumption spiked drastically. 
4. June and November are months that are very likely to experience more number of rainy days and higher wet bulb temperatures, based on the moderately positive correlations of both variables to electricity consumption, these are months EMA needs to pay attention to in terms of electricity demand planning.

### Conclusion

Due to the moderately positive correlation between wet bulb temperature and electricity consumption, and a mild positive correlation between temperature and electricity consumption, we can posit that electricity consumption will continue to increase as global temperatures increase. It is important that EMA takes temperature and rainfall into account when planning for electricity supply. This has to be caveated that correlation does not imply causation, more studies need to be done to identify other factors that were not included in this analysis that possibly affects electricity consumption. 

In addition, there may be instances where a spike in electricity consumption cannot be planned for, such as when a global pandemic event occurs and people are forced to stay indoors to control the spread of virus.

Lastly, June and November are months to look out for where domestic electricity consumption may be higher due to increased wet bulb temperatures and number of rainy days.

### Recommendations
Global temperatures are expected to increase by 0.4°C by 2030 [(New York Times, 2023)](https://www.nytimes.com/2023/03/20/climate/global-warming-ipcc-earth.html) while Singapore's population is expected to be between 6.5-6.9M in the same year[(Straits Times, 2024)](https://www.straitstimes.com/singapore/singapores-population-could-hit-69m-by-2030), a 26.6% increase from the current population of 5.45M. 

Assuming dwelling units increase proportionately to population, and taking into account the correlation coefficient between temperature and electricity consumption, the demand for electricity is expected to increase by **27.1% for private housing and 27.3% for public housing**. 

In addition, as burning of fuels for energy generation play a large role in global warming, we also have to ensure that we rely on cleaner forms of energy to meet the increased demand, such that we do not create a vicious cycle electricity consumption that leads to higher temperatures. 

I would also recommend to test the hypotheses on temperature and rainy days against electricity consumption. If the null hypothesis can be rejected with a 95% confidence level, we can use this data to build more accurate predictive models for housing electricity consumption planning.
