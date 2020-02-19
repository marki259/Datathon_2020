library(sp)
library(leaflet)
library(dplyr)
library(httr)
library(tidyverse)

setwd('/home/marc/School/Datathon_2020')
tw_dat <- read.csv('trafficWeather_dat.csv', stringsAsFactors=FALSE)

##Take a day 
head(tw_dat$date)

tw_sub <- subset(tw_dat, date == "2019-11-30" & period == 'Peak')

m <- leaflet() %>% addTiles()

tw_sub$logTotal <- log(tw_sub$car + tw_sub$lorry + 1)

pal <- colorNumeric(
  palette = "Blues",
  domain = tw_sub$logTotal)

m %>% 
  addCircleMarkers(tw_sub$lng, tw_sub$lat, color=pal(tw_sub$logTotal))


