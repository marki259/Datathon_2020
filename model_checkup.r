library(lme4)
library(BBmisc)

setwd('/home/marc/School/Datathon_2020')
tw_dat <- read.csv('trafficWeather_dat.csv', stringsAsFactors=FALSE)

tw_dat$total <- tw_dat$car + tw_dat$lorry

#two-level Poisson model with segment as the random effect
hist(tw_dat$total, nclass=100, col = 2)
quantile(tw_dat$total)

mean(tw_dat$total)

model1.fit <- glmer(formula = total ~ 1 + (1|segment_id), 
                    data=tw_dat,
                    family="poisson",
                    na.action=na.exclude)
summary(model1.fit)

hist(exp(predict(model1.fit)))


trafficWeather_dat$prediction <- predict(model1.fit, newdata=trafficWeather_dat)

hist(prediction, nclass=100, col = 3)

library(tsp)
