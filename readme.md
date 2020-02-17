# DATATHON: FISHER's TUNAS

## Guidelines & Downloads

* Leuven air data: https://data.leuvenair.be/data-l.html
* Traffic sensors API documentation: https://documenter.getpostman.com/view/5886213/S11RLFhq/?version=latest
* traffic.csv uploaded
* Leuven weather data: https://data.leuvenair.be/data-g.html

## Some data info

* Traffic per segment data API is pretty painless.
* The traffic data is very rare in Leuven, most in Kessel-lo and elsewhere in Belgium e.g. Antwerp.  
* Apparently lot's of data but should be aggregated depending on our goals. 
* Around 1 and a half year of historical data available (all-around). Something like that anyway. Only about 7 months of weather data actually.
* The airdata is concentrated in and around Leuven e.g. Kessel-lo and Heverlee. Similar dispersion with the weather sensors. 

## Project ideas (Bring it on)

1. ~A list of the best walking paths in Leuven~
This idea is scrapped (not enough data in Leuven, but mbe elsewhere?)
  * Forecasting for next days? 
  * Building a cost function
  * Genetic algo (or other heuristic for path selection)
  * Uses GPS segment data along with traffic, PM and weather data
  * We could subset selection based on amounts of KMs, time of day etc. 
  * (Pedestrian + Bike)/Car ratio could a useful variable
 
2. Predicting pedestrian and bike traffic in Leuven from weather and 2.5 pollution data (we don't even have to predict, even simpler is just providing estimation for past quantities)
 * There are very few traffic sensor in Leuven itself, but we can use info from Kessel-Lo or similar regions to train model
 * The weather and pollution at a traffic sensor could be treated as weighted mean based on distance of that traffic sensor from the neighboring weather and pollution sensors (euclidean distance of x and y gps (I don't think we have to correct for earth rotation for small distances)
 * For the map, it probably wouldn't be to hard to allow filtering of predictions for pedestrian and bikes (see Telraam)

## Miscalleneous

The Postman software can be installed on windows to easily try out API queries. 
