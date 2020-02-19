library(lme4)
library(BBmisc)
library (Metrics)

names(trafficWeather_dat)

library("PerformanceAnalytics")
cor <- trafficWeather_dat[, c(11,12,13,14,15)]
p<-chart.Correlation(cor, histogram=TRUE, pch=19)
p

trafficWeather_dat$total <- trafficWeather_dat$car + trafficWeather_dat$lorry 
hist(trafficWeather_dat$total, nclass=100, col = 2)

attach(trafficWeather_dat)
par(mfrow=c(2,2))
hist(bike, nclass=100, main='bike', col=2)
hist(car, nclass=100, main='car', col=2)
hist(lorry, nclass=100, main='lorry', col=2)
hist(pedestrian, nclass=100, main='pedestrian', col=2)


sum(trafficWeather_dat$total == 0) #403 zero values


#normalization 

trafficWeather_dat$TEMPC_n <- normalize(trafficWeather_dat$TEMPC, method = "standardize", range = c(0, 1), margin = 1L, on.constant = "quiet")
trafficWeather_dat$HUMIDITY_n <- normalize(trafficWeather_dat$HUMIDITY, method = "standardize", range = c(0, 1), margin = 1L, on.constant = "quiet")
trafficWeather_dat$WINDSPEEDKMH_n <- normalize(trafficWeather_dat$WINDSPEEDKMH, method = "standardize", range = c(0, 1), margin = 1L, on.constant = "quiet")
trafficWeather_dat$WINDCHILLF_n <- normalize(trafficWeather_dat$WINDCHILLF, method = "standardize", range = c(0, 1), margin = 1L, on.constant = "quiet")
trafficWeather_dat$RAININ_n <- normalize(trafficWeather_dat$RAININ, method = "standardize", range = c(0, 1), margin = 1L, on.constant = "quiet")

hist(trafficWeather_dat$WINDSPEEDKMH_n)

#converting date to day of the week
library(lubridate)
date<-ymd(trafficWeather_dat$date)
trafficWeather_dat$dow<-wday(date) #7 Saturday 1 Sunday
trafficWeather_dat$weekend<-ifelse(trafficWeather_dat$dow==1|trafficWeather_dat$dow==7,1,0)


#split the dataset
set.seed(101)
sample <-sample.int(n=nrow(trafficWeather_dat),size=floor(0.75*nrow(trafficWeather_dat)),replace=F)
train<-trafficWeather_dat[sample,]
test<-trafficWeather_dat[-sample,]
                    


#two-level Poisson model with segment as the random effect
model.fit <- glmer(formula = total ~ 1 + TEMPC_n+ HUMIDITY_n+WINDSPEEDKMH_n+RAININ_n+
                     factor(weekend)+factor(period)+
                    (1|segment_id), 
                    data=train,
                    family="poisson",
                    na.action=na.exclude)
summary(model.fit)


#prediction
test$prediction <- exp(predict(model.fit, newdata=test, allow.new.levels=TRUE))

mode

#visulize in a joint hist
p1 <-hist(test$total, nclass=100)
p2 <- hist(test$prediction, nclass=100)
plot( p1, col=rgb(0,0,1,1/4), xlim=c(0,10000))  # first histogram
plot( p2, col=rgb(1,0,0,1/4), xlim=c(0,10000), add=T) 

