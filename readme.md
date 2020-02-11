# DATATHON: FISHER's TUNAS

## Guidelines & Downloads

* Leuven air data: https://data.leuvenair.be/data-l.html
* Traffic sensors API documentation: https://documenter.getpostman.com/view/5886213/S11RLFhq/?version=latest
* Leuven weather data: https://data.leuvenair.be/data-g.html

## Some data info

* Traffic per segment data API is pretty painless.
* The traffic data is very rare in Leuven, most in Kessel-lo and elsewhere in Belgium e.g. Antwerp.  
* Apparently lot's of data but should be aggregated depending on our goals. 
* Around 1 and a half year of historical data available (all-around). Something like that anyway. 
* The airdata is concentrated in and around Leuven e.g. Kessel-lo and Heverlee. 

## Project ideas (Bring it on)

1. ~A list of the best walking paths in Leuven~
This idea is scrapped (not enough data in Leuven, but mbe elsewhere?)
  * Forecasting for next days? 
  * Building a cost function
  * Genetic algo (or other heuristic for path selection)
  * Uses GPS segment data along with traffic, PM and weather data
  * We could subset selection based on amounts of KMs, time of day etc. 
  * (Pedestrian + Bike)/Car ratio could a useful variable

## Miscalleneous

The Postman software can be installed on windows to easily try out API queries. 
