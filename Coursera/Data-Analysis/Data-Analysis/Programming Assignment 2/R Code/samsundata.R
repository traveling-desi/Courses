setwd("/Users/sarpotd/Desktop/Coursera/Data Analysis/Programming Assignment 2/")
load("R Data/samsungData.rda")


sd <- samsungData
names(sd) <- gsub("\\)","",names(sd))
names(sd) <- gsub("\\(","",names(sd))
names(sd) <- make.names(names(sd),unique =TRUE)
testset_sd <- sd[sd$subject%in%c(27,28,29),]
testset_sd <- subset(testset_sd,select=-subject)
trainset_sd <- sd[!sd$subject%in%c(27,28,29),]
trainset_sd <- subset(trainset_sd,select=-subject)

set.seed(123)

library(tree)
tree1 <- tree(as.factor(activity) ~ ., trainset_sd)
cv_tree <- cv.tree(tree1)
par(mfrow=c(2,1))
plot(tree1, col="blue",type="uniform")
text(tree1,cex=0.65,col="red")
plot(cv_tree,main="Deviance Reduction with Growth of Tree", sub="Figure 1")
dev.copy2pdf(file="test.pdf")

pruned <- prune.tree(tree1,best=8)
plot(pruned, col="blue",type="uniform")
text(pruned,col="red")
summary(tree1)
summary(pruned)
table1 <- table(predict(tree1,newdata=testset_sd,type="class"), testset_sd$activity)
table1
sum(table1[row(table1) != col(table1)])/sum(table1)
table1 <- table(predict(pruned,newdata=testset_sd,type="class"), testset_sd$activity)
table1
sum(table1[row(table1) != col(table1)])/sum(table1)



library(ipred)
bagTree <- bagging(as.factor(activity) ~ ., trainset_sd, coob=TRUE)
print(bagTree)

library(randomForest)
system.time(forest_sd <- randomForest(as.factor(activity) ~ ., data=trainset_sd, prox=TRUE, ntree=150, importance=T))
system.time(forest_sd_1 <- randomForest(as.factor(activity) ~ tGravityAcc.mean.X  +  tGravityAcc.min.X   + angleX.gravityMean + tGravityAcc.max.X   + angleY.gravityMean + tGravityAcc.min.Y  + tGravityAcc.mean.Y  +  tGravityAcc.energy.X  + tGravityAcc.max.Y + tGravityAcc.energy.Y + fBodyAccJerk.energy.X  + angleZ.gravityMean + tBodyAccJerk.mad.X  + fBodyAccMag.std +  fBodyAccJerk.bandsEnergy.1.16 + tGravityAcc.arCoeff.X.1 + tBodyAccJerk.std.X + tGravityAcc.max.Z  + tGravityAcc.mean.Z  + tBodyAccJerkMag.entropy + tBodyAcc.max.X + tGravityAcc.arCoeff.Z.1 + tBodyGyroJerk.iqr.Z + tBodyAccMag.mad + tGravityAcc.min.Z + tBodyAccJerk.energy.X + tGravityAccMag.mad + tGravityAcc.arCoeff.Y.2  + fBodyAccJerk.energy.Y  + tBodyAccMag.arCoeff1, data=trainset_sd, prox=TRUE, ntree=150, importance=T))
forest_sd_1
par(mfrow=c(2,1))
varImpPlot(forest_sd)
dev.copy2pdf(file="test1.pdf")
plot(forest_sd,type="l", main="Progression of OOB error with # of trees")
dev.copy2pdf(file="test2.pdf")

tree_sd_1 <- tree(as.factor(activity) ~ tGravityAcc.mean.X  +  tGravityAcc.min.X   + angleX.gravityMean + tGravityAcc.max.X   + angleY.gravityMean + tGravityAcc.min.Y  + tGravityAcc.mean.Y  +  tGravityAcc.energy.X  + tGravityAcc.max.Y + tGravityAcc.energy.Y + fBodyAccJerk.energy.X  + angleZ.gravityMean + tBodyAccJerk.mad.X  + fBodyAccMag.std +  fBodyAccJerk.bandsEnergy.1.16 + tGravityAcc.arCoeff.X.1 + tBodyAccJerk.std.X + tGravityAcc.max.Z  + tGravityAcc.mean.Z  + tBodyAccJerkMag.entropy + tBodyAcc.max.X + tGravityAcc.arCoeff.Z.1 + tBodyGyroJerk.iqr.Z + tBodyAccMag.mad + tGravityAcc.min.Z + tBodyAccJerk.energy.X + tGravityAccMag.mad + tGravityAcc.arCoeff.Y.2  + fBodyAccJerk.energy.Y  + tBodyAccMag.arCoeff1, data=trainset_sd)

table1 <- table(predict(forest_sd_1,newdata=testset_sd,type="class"), testset_sd$activity)
sum(table1[row(table1) != col(table1)])/sum(table1)
sum(predict(forest_sd_1,newdata=testset_sd) != testset_sd$activity)/length(testset_sd$activity)

                      
forest_sd <- randomForest(as.factor(activity) ~ fBodyAccJerk.bandsEnergy.1.16 + tGravityAcc.min.X + fBodyAccMag.mad + tGravityAcc.arCoeff.Z.2 + angleY.gravityMean, data=trainset_sd, prox=TRUE, ntree=50)
forest_sd


library(e1071)

trainset_sd_pruned <- trainset_sd[,c("fBodyAccJerk.bandsEnergy.1.16","tGravityAcc.min.X","fBodyAccMag.mad","tGravityAcc.arCoeff.Z.2","angleY.gravityMean","activity")]
trainset_sd_tuned <- tune.svm(as.numeric(as.factor(activity))~., data = trainset_sd_pruned, gamma = 10^(-6:-1), cost = 10^(-1:1))
summary(trainset_sd_tuned)
trainset_sd_tuned <- tune.svm(as.numeric(as.factor(activity))~., data = trainset_sd_pruned, gamma = 10^(-1:1), cost = 10^(1:2))
summary(trainset_sd_tuned)
trainset_sd_tuned <- svm(as.numeric(as.factor(activity))~., data = trainset_sd_pruned, kernel ="radial", gamma = 1, cost = 100)




## test
prediction<- predict(trainset_sd_tuned,testset_sd[,-563])
tab <- table(pred = prediction, true = testset_sd[,563])




### Not used from here:

subset(sd,subject==1,grep("*",names(sd)))
lm1 <- lm(as.numeric(as.factor(activity)) ~ fBodyAccJerk.bandsEnergy.1.16 + tGravityAcc.min.X + fBodyAccMag.mad + tGravityAcc.arCoeff.Z.2 + angleY.gravityMean, data=trainset_sd)
plot(lm1)
plot(as.factor(trainset_sd$activity),trainset_sd$fBodyAccJerk.bandsEnergy.1.16)
plot(as.factor(trainset_sd$activity),trainset_sd$tGravityAcc.min.X)
plot(as.factor(trainset_sd$activity),trainset_sd$fBodyAccMag.mad)
plot(as.factor(trainset_sd$activity),trainset_sd$tGravityAcc.arCoeff.Z.2)
plot(as.factor(trainset_sd$activity),trainset_sd$angleY.gravityMean)

> trainset_sd_tuned <- tune.svm(as.numeric(as.factor(activity))~., data = trainset_sd_pruned, gamma = 10^(-6:-1), cost = 10^(-1:1))
> summary(trainset_sd_tuned)

Parameter tuning of ‘svm’:

- sampling method: 10-fold cross validation 

- best parameters:
 gamma cost
   0.1   10

- best performance: 0.150627 

- Detailed performance results:
   gamma cost     error dispersion
1  1e-06  0.1 2.8763438 0.10587958
2  1e-05  0.1 2.7722747 0.10200243
3  1e-04  0.1 1.8819511 0.06930956
4  1e-03  0.1 0.7068497 0.03330825
5  1e-02  0.1 0.4280717 0.02405933
6  1e-01  0.1 0.2074739 0.01603386
7  1e-06  1.0 2.7722689 0.10200207
8  1e-05  1.0 1.8809584 0.06926114
9  1e-04  1.0 0.7132805 0.03390252
10 1e-03  1.0 0.5244333 0.03052157
11 1e-02  1.0 0.3009506 0.02325996
12 1e-01  1.0 0.1784225 0.01610935
13 1e-06 10.0 1.8808558 0.06925453
14 1e-05 10.0 0.7139769 0.03395955
15 1e-04 10.0 0.5448095 0.03235767
16 1e-03 10.0 0.4158480 0.02920683
17 1e-02 10.0 0.2464809 0.02152447
18 1e-01 10.0 0.1506270 0.01481042

> trainset_sd_tuned <- tune.svm(as.numeric(as.factor(activity))~., data = trainset_sd_pruned, gamma = 10^(-1:1), cost = 10^(1:2))
> summary(trainset_sd_tuned)

Parameter tuning of ‘svm’:

- sampling method: 10-fold cross validation 

- best parameters:
 gamma cost
     1  100

- best performance: 0.1126935 

- Detailed performance results:
  gamma cost     error dispersion
1   0.1   10 0.1509228 0.01380338
2   1.0   10 0.1127767 0.01145628
3  10.0   10 0.2450982 0.02814922
4   0.1  100 0.1364676 0.01228605
5   1.0  100 0.1126935 0.01022366
6  10.0  100 0.2964076 0.04378204


data(Cars93,package="MASS")
set.seed(7363)
cars1 <- Cars93[sample(1:dim(Cars93)[1], replace=T),]
cars2 <- Cars93[sample(1:dim(Cars93)[1], replace=T),]
cars3 <- Cars93[sample(1:dim(Cars93)[1], replace=T),]
tree1 <- tree(DriveTrain ~ Price + Type, data=cars1)
tree2 <- tree(DriveTrain ~ Price + Type, data=cars2)
tree3 <- tree(DriveTrain ~ Price + Type, data=cars3)
newdata = data.frame(Type = "Large",Price = 20)
predict(tree1,newdata,type="class")
predict(tree2,newdata,type="class")
predict(tree3,newdata,type="class")


sum(predict(forest_sd_1,newdata=testset_sd) != testset_sd$activity)/length(testset_sd$activity)



system.time(forest_sd_2 <- randomForest(as.factor(activity) ~ 
 
tGravityAcc.min.X   + 
tGravityAcc.mean.X  +  
tGravityAcc.max.X   + 
tGravityAcc.energy.X  + 
tGravityAcc.min.Y  + 
tGravityAcc.mean.Y  +  
tGravityAcc.max.Y + 
tGravityAcc.energy.Y +
tGravityAcc.min.Z  + 
tGravityAcc.mean.Z  + 
tGravityAcc.max.Z + 
tGravityAcc.energy.Z +
 
 
angleX.gravityMean + 
angleY.gravityMean + 
angleZ.gravityMean + 
 
 
fBodyAccJerk.energy.X  + 
fBodyAccJerk.energy.Y  + 
fBodyAccJerk.energy.Z  + 
 
tBodyAcc.correlation.X.Y +
tBodyAcc.correlation.X.Z +
tBodyAcc.correlation.Y.Z +
 
 
tGravityAcc.arCoeff.X.1 +
tGravityAcc.arCoeff.X.2 +
tGravityAcc.arCoeff.X.3 +
tGravityAcc.arCoeff.X.4 +
tGravityAcc.arCoeff.Y.1 +
tGravityAcc.arCoeff.Y.2 +
tGravityAcc.arCoeff.Y.3 +
tGravityAcc.arCoeff.Y.4 +
tGravityAcc.arCoeff.Z.1 +
tGravityAcc.arCoeff.Z.2 +
tGravityAcc.arCoeff.Z.3 +
tGravityAcc.arCoeff.Z.4 +
fBodyAcc.bandsEnergy.1.8, data=trainset_sd, prox=TRUE, ntree=150, importance=T))


   user  system elapsed 
 33.891   0.523  34.283 
> sum(predict(forest_sd_2,newdata=testset_sd) != testset_sd$activity)/length(testset_sd$activity)
[1] 0.06805808
> system.time(forest_sd <- randomForest(as.factor(activity) ~ ., data=trainset_sd, prox=TRUE, ntree=150, importance=T))
   user  system elapsed 
137.284   1.358 139.008 
> sum(predict(forest_sd,newdata=testset_sd) != testset_sd$activity)/length(testset_sd$activity)
[1] 0.04446461