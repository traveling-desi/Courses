###################################################################################################


### Recommendation

require(plyr)
require(reshape2)
setwd("/Users/sarpotd/Desktop/Coursera/Big Data in Education/week3/Assignment1/")
actions <- read.csv("bigdata-edu-Data-Sets-Data-Subset-Pardos-et-al-2013-actions - Week 3A.csv" , header=TRUE)
actions_colnames <- colnames(actions)
actions_colnames[3] <- "UserID"
actions_colnames[39] <- "ObsID"
colnames(actions) <- actions_colnames

obs <- read.csv("bigdata-edu-Data-Sets-Data-Subset-Pardos-et-al-2013-observations Week 3B.csv", header=TRUE)
colnames(obs)<- c("ObsID","UserID","probID","date","coder","AFFECT","BEHAVIOR")

#1
gaming_mat <- table(obs$UserID,obs$BEHAVIOR)
gaming_mat[order(gaming_mat[,"GAMING"]/apply(gaming_mat,1,sum), decreasing=TRUE),]

#2
bored_mat <- table(obs$UserID,obs$AFFECT)
table(bored_mat[,"BORED"]<=0)

#3
student_mat <- obs[obs$date=="10/15/1900"&obs$UserID==30314880,]


#4
table(actions$problemId)
There arent enough repeated problems in the dataset

#5
obs_mat <- as.matrix(table(actions$ObsID))
sum(obs_mat[,1])/nrow(obs_mat)


#6
obs_mat_sort <- as.matrix(obs_mat[order(obs_mat[,1],decreasing=TRUE),])
sum(obs_mat_sort[3:nrow(obs_mat_sort),1])/(nrow(obs_mat_sort)-2)



#7
obs2_mat <- actions[actions$ObsID=="MFDTT-mathasst-9-at_12:58:03-79",]
sum(obs2_mat$timeTaken)/nrow(obs2_mat)


#8
obs3_mat <- actions[actions$ObsID=="EGMDH-math_assistments-4-at_10:34:30-9",]

