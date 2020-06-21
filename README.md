# Crowdedness-Map

The goal of this project is to create a map-based application which summarizes recent data on the crowdedness of establishments (restaurants, stores, churches, etc.) and, within each establishment, the most crowded days and hours. This will allow users to avoid the busiest places and times. Although crowdedness is not a perfect measure of disease transmission risk, it is an important contributor. So, this application will be one tool that people can use to reduce the risk of getting or spreading COVID-19. 

The raw data were obtained from [Veraset](https://www.veraset.com/). They contain ping-level cell phone location data from a 5% sample of cell phones in America from the last four weeks (updated weekly).

We define crowdedness as follows:
1. For every minute of data beginning at 8:00 a.m. and ending at 10 p.m. each day, we compute how many cell phones in our sample are present in each establishment.
1. We multiply this number by 20 (since we have a 5% sample). This gives us an estimated number of individuals present at the establishment -- call this number *N*.
1. We multiply *N* by *N - 1* to get the number of potential contacts for each minute in each establishment.
1. We divide the number of potential contacts by the square footage of the establishment to get the number of potential contacts per square foot.
1. We sum this number by hour of day, day of week, and over the whole four-week sample to get the crowdedness of each establishment in those time intervals.
1. We divide these numbers by the total estimated number of visitors to the establishment in the given hour of day, day of week, and over the whole four-week sample to get the average crowdedness per visitor in those time intervals.
1. All rankings and comparisons in the application are based on these average crowdedness per visitor values, and all rankings are within a [commuting zone](https://en.wikipedia.org/wiki/Commuting_zone).

## Data

The input data for the application are contained in csv with the following variables:
* location_name: The name of the establishment (e.g. McDonald's, Target)
* latitude, longitude: The latitude and longitude of the establishment
* grocery, restaurant: Indicator for whether or not the establishment is a grocery store (NAICS code 4451) or restaurant (NAICS code 7225)
* unreliable: Indicator for unreliable data (NAICS codes 23 or 42, no reliable square footage value, and/or >15% of dwell time >=12 hours)
* crowded_place: In which third of the crowdedness distribution within the establishment's commuting zone the establishment falls (0 = bottom third, 1 = middle third, 2 = top third)
* crowded_grocery: Only defined for grocery stores -- in which third of the crowdedness distribution for grocery stores within the establishment's commuting zone the establishment falls in
* crowded_restaurant: Only defined for restaurants -- in which third of the crowdedness distribution for restaurants within the establishment's commuting zone the establishment falls in
* comp_to_grocery: How crowded the establishment is relative to the mean crowdedness of grocery stores in the establishment's commuting zone (0 = <1/2 the mean, 1 = >=1/2 the mean <=2 times the mean, 2 = >2 times the mean)
* hofd<#>, with # = 1-6: the most crowded hours of the day for the establishment (8 = 8 a.m. to 9 a.m., 9 = 9 a.m. to 10 a.m., etc.); hofd1 is the most crowded hour, hofd2 is the second-most crowded hour, and so on
* dofw<#>, with # = 1-3: the most crowded days of the week for the establishment (0 = Sunday, 1 = Monday, etc.); dofw1 is the most crowded day, dofw2 is the second-most crowded day, and so on

In order to be considered a most crowded hour of day or day of week, the hour/day must be at least 1.5 times as crowded as the mean hour/day for the establishment and at least 0.9 times as crowded as the most crowded hour/day of the establishment. So, some establishments have more croweded hours/days than others. No most crowded hour/day is reported for establishments that receive fewer than 20 visits in the four weeks of the sample.
