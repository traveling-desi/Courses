
#############################################################################

###  This program is written in R. It is fully executable as written in a R environment


#############################################################################


## Require packages and read in the the data collateral provided.

require(plyr)
require(reshape2)
setwd("/Users/sarpotd/Desktop/Coursera/Recommender Systems/week4/Assignment2/")
ratings <- read.csv("data/ratings.csv", header=FALSE)
colnames(ratings) <- c("user_id", "movie_id", "ratings")
users <- read.csv("data/users.csv", header=FALSE)
colnames(users) <- c("user_id", "user_name")
movies <- read.csv("data/movie-titles.csv", header=FALSE)
colnames(movies) <- c("movie_id", "movie_name")


## Data munging to change it to a form useful for manipulation
## user_ratings as ratings of users for movies in a matrix form.

temp_1 <- melt(ratings, id=c("user_id","movie_id"), measure="ratings")
temp_2 <- acast(temp_1, user_id ~ movie_id ~ variable)
user_ratings <- as.matrix(temp_2[,,1])

## Backup copy of the user_ratings matrix before we do data munging on it.

user_ratings_rownames <- rownames(user_ratings)
user_ratings_bak <- user_ratings
user_ratings_bak[is.na(user_ratings)] = 0


## Calculate mean for all users. Omit any "NA"

mean_calc <- function(c) (mean(na.omit(c)))
user_ratings_mean <- as.matrix(apply(user_ratings,1,mean_calc))
rownames(user_ratings_mean) <- user_ratings_rownames

## Subtract means for all users from their individual ratings for each item.
## This gets us mean centered ratings.

sub_mean <- function(c) (c - user_ratings_mean)
temp_1 <- apply(user_ratings_bak,2,sub_mean)
rownames(temp_1) <- user_ratings_rownames
user_ratings_mean_centered <- temp_1
user_ratings_mean_centered[is.na(user_ratings)] = 0

## Calculate Euclidean Norm for each user using their mean centered ratings.

norm_calc <- function(c) (sqrt(sum(c^2)))
user_ratings_norm <- as.matrix(apply(user_ratings_mean_centered,1,norm_calc))
rownames(user_ratings_norm) <- user_ratings_rownames


## Create a list fo the users and movies assigned to us

input_user_list <- c(rep("3230",times=5),rep("5201",times=5),rep("912",times=5),rep("348",times=5),rep("651",times=5))
input_item_list <- c("329","38","197","955","7443","585","1637","1900","85","2502","8587","462","9806","141","278","146","22","752","63","268","12","664","10020","671","8358")


### This is the meat of the program. A function called final_fun is written
### This is a function to calcualte the cosine similarity with each input_user, find the top 30 "similar" neighbors that have rated the input_item
### Then find the prediction based on the formula given the instructions of the assignment.


final_fun <- function(c) {
input_user <- input_user_list[c]
input_item <- input_item_list[c]
cosine_fun <- function(c) (sum(c*user_ratings_mean_centered[input_user,]))
temp <- as.matrix(apply(user_ratings_mean_centered,1,cosine_fun))
rownames(temp) <- user_ratings_rownames
norm_fun <- function(c) (temp[c]/(user_ratings_norm[input_user,]*user_ratings_norm[c]))
cos_similarity <- data.frame(mapply(norm_fun,1:nrow(temp)))
rownames(cos_similarity) <- user_ratings_rownames
cos_similarity[,2] <- rownames(cos_similarity)
cos_similarity <- cos_similarity[!is.na(user_ratings[,input_item]),]
colnames(cos_similarity) <- c("cosine","user")
cos_similarity <- cos_similarity[order(cos_similarity$cosine,decreasing=TRUE),]

neighbors <- (cos_similarity[cos_similarity$user!=input_user,])[1:30,]

print(input_user)
print(input_item)
print(user_ratings_mean[input_user,] + (sum(cos_similarity[rownames(neighbors),"cosine"] * user_ratings_mean_centered[rownames(neighbors),input_item])/sum(abs(cos_similarity[rownames(neighbors),"cosine"]))))
print(movies[movies$movie_id==input_item,"movie_name"])
}


### Call the final_fun function on each of the user:movie combination iteratively.

mapply(final_fun,1:length(input_user_list))