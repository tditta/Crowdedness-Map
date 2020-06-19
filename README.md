# Crowdedness-Map

The goal of this project is to create a map-based application which summarizes recent data on the crowdedness of establishments (restaurants, stores, churches, etc.) and, within each establishment, the most crowded days and hours. This will allow users to avoid the busiest places and times. Although crowdedness is not a perfect measure of disease transmission risk, it is an important contributor. So, this application will be one tool that people can use to reduce the risk of getting or spreading COVID-19. 

The data were obtained from [Veraset](https://www.veraset.com/). They contain ping-level cell phone location data from a 5% sample of cell phones in America from the last four weeks (updated weekly).

We define crowdedness as follows:
1. For every minute of data, we compute how many cell phones in our sample are present in each establishment.
1. We multiply this number by 20 (since we have a 5% sample). This gives us an estimated number of individuals present at the establishment -- call this number *N*.
1. We multiply *N* by *N - 1* to get the number of potential contacts for each minute in each establishment.
1. We divide the number of potential contacts by the square footage of the establishment to get the number of potential contacts per square foot.
1. We sum this number by hour of day, day of week, and over the whole four-week sample to get the crowdedness of each establishment in those time intervals.
1. We divide these numbers by the total estimated number of visitors to the establishment in the given hour of day, day of week, and over the whole four-week sample to get the average crowdedness per visitor in those time intervals.
1. All rankings and comparisons in the application are based on these average crowdedness per visitor values.
