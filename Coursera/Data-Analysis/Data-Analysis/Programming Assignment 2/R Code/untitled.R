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
tGravityAcc.arCoeff.Z.4


,data=trainset_sd, prox=TRUE, ntree=150, importance=T))
