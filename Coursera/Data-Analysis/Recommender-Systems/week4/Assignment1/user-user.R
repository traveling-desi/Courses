require(plyr)
require(reshape2)
setwd("/Users/sarpotd/Desktop/Coursera/Recommender Systems/week4/Assignment1/")
movies <- read.csv("recsys-data-sample-rating-matrix.csv", header=FALSE)
colnames(movies) <- movies[1,]
rownames(movies) <- movies[,1]
movies <- movies[2:nrow(movies),2:ncol(movies)]


mean_calc <- function(c) (mean(na.omit(c)))
sd_calc <- function(c) (sd(na.omit(c)))
user_ratings_mean <- as.matrix(apply(movies,2,mean_calc))
user_ratings_sd <- as.matrix(apply(movies,2,sd_calc))
user_ratings <- as.matrix(movies)
user_ratings_colnames <- colnames(user_ratings)
user_ratings[is.na(movies)] = 0

mean_sub <- function(c) ( (user_ratings[,c] - user_ratings_mean[c]) )
user_ratings <- mapply(mean_sub,1:ncol(user_ratings))
user_ratings[is.na(movies)] = 0
colnames(user_ratings) <- user_ratings_colnames

user_corr <- matrix(data = NA, nrow=ncol(user_ratings), ncol=ncol(user_ratings))



for (a in 1:ncol(user_ratings))
	for (b in 1:ncol(user_ratings)) {
		user_corr[a,b] <- (sum(user_ratings[,a]*user_ratings[,b]))/(user_ratings_sd[a]*user_ratings_sd[b])
		user_corr[b,a] <- user_corr[a,b]
	}
