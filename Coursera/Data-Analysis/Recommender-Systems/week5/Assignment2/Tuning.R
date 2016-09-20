
## Require packages and read in the the data collateral provided.

require(ggplot2)
require(data.table)

setwd("/Users/sarpotd/Desktop/Coursera/Recommender Systems/week5/Assignment2/")
results <- data.table(read.csv("eval-assignment/target/analysis/eval-results.csv"))




ggplot(results[,list(RMSE=mean(RMSE.ByUser)),by=list(Algorithm,NNbrs)][,list(Name=paste(Algorithm,NNbrs),Algorithm,NNbrs,RMSE)]) +

    aes(x=Name, y=RMSE) +

    geom_boxplot() +

# The following line rotates labels on the x-axis vertically.

    theme(axis.text.x=element_text(angle=90,hjust=1,vjust=0.5))




Question 2

temp <- results[,list(RMSE=mean(RMSE.ByUser)),by=list(Algorithm,NNbrs)]
temp_L <- temp[temp$Algorithm == "LuceneNorm",]
plot(temp_L$NNbrs,temp_L$RMSE,type= "n")
plot(temp_L$NNbrs,temp_L$RMSE,type= "l")
points(51,0.825613,pch=3)
points(40,0.825613,pch=3)
points(43,0.825613,pch=3)
points(44,0.825613,pch=3)




Question 3

temp <- results[,list(nDCG=mean(nDCG)),by=list(Algorithm,NNbrs)]
temp_L <- temp[temp$Algorithm == "LuceneNorm",]
plot(temp_L$NNbrs,temp_L$nDCG,type= "n")
plot(temp_L$NNbrs,temp_L$nDCG,type= "l")
points(51,0.9618028,pch=3)
points(75,0.9618028,pch=3)


Question 4

ggplot(results[,list(RMSE=mean(RMSE.ByUser)),by=list(Algorithm,NNbrs)][,list(Name=paste(Algorithm,NNbrs),Algorithm,NNbrs,RMSE)]) +

    aes(x=Name, y=RMSE) +

    geom_boxplot() +

# The following line rotates labels on the x-axis vertically.

    theme(axis.text.x=element_text(angle=90,hjust=1,vjust=0.5))




    ggplot(results[,list(nDCG=mean(nDCG)),by=list(Algorithm,NNbrs)][,list(Name=paste(Algorithm,NNbrs),Algorithm,NNbrs,nDCG)]) +

    aes(x=Name, y=nDCG) +

    geom_boxplot() +

# The following line rotates labels on the x-axis vertically.

    theme(axis.text.x=element_text(angle=90,hjust=1,vjust=0.5))




Question 8



    ggplot(results[,list(TestTime=mean(TestTime)),by=list(Algorithm,NNbrs)][,list(Name=paste(Algorithm,NNbrs),Algorithm,NNbrs,TestTime)]) +

    aes(x=Name, y=TestTime) +

    geom_boxplot() +

# The following line rotates labels on the x-axis vertically.

    theme(axis.text.x=element_text(angle=90,hjust=1,vjust=0.5))


and

temp <- results[,list(Coverage=mean(Coverage),RMSE=mean(RMSE.ByUser),nDCG=mean(nDCG),TopN.nDCG=mean(TopN.nDCG)),by=list(Algorithm,NNbrs)]





Question 9

temp <- results[,list(Coverage=mean(Coverage),RMSE=mean(RMSE.ByUser),nDCG=mean(nDCG),TopN.nDCG=mean(TopN.nDCG)),by=list(Algorithm,NNbrs)]





    Question 12

    mean(results[results$Algorithm == "Popular",TopN.nDCG])
