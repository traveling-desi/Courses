
setwd("/Users/sarpotd/Desktop/Coursera/Data Analysis/Programming Assignment 1/R Code/")
loansData <- read.csv("../R Data/loansData.csv", as.is=TRUE)
par(mfrow=c(1,2))

rownames(loansData) <- NULL
par(ask=TRUE)

loansData$Interest.Rate <- as.numeric(gsub("%","",loansData$Interest.Rate))
loansData$Debt.To.Income.Ratio <- as.numeric(gsub("%","",loansData$Debt.To.Income.Ratio))
loansData <- loansData[order(loansData$Interest.Rate),]

loansData <- na.omit(loansData)
loansData[loansData$Employment.Length == "n/a","Employment.Length"] <- "< 1 year"



loansData$FICO <- apply(sapply(strsplit(loansData$FICO.Range, "-"), function(x) as.numeric(x)), 2, mean)
loansData$FICO_4_ranges <- cut(loansData$FICO,4)



temp <- tapply(loansData$Interest.Rate,loansData$FICO_4_ranges)
loansData_642_689 <- loansData[temp==1,]
loansData_689_737 <- loansData[temp==2,]
loansData_737_785 <- loansData[temp==3,]
loansData_785_832 <- loansData[temp==4,]


coplot(loansData$Interest.Rate ~ jitter(loansData$Inquiries.in.the.Last.6.Months, factor=3) |loansData$Loan.Length, col=loansData$FICO_4_ranges, pch=19,columns=2,xlab=c("Inquiries in the last 6 Months", paste("Factor Based Plot Showing Interest Rates charged for each Loan Length")), ylab="Interest Rate",xlim=c(0,6))
mtext(text=". Fico Score: 642-689",side=1,line=1,col="black",las=1,padj=0,at=0,adj=1)
mtext(text=". Fico Score: 689-737",side=1,line=1,col="red",las=1,padj=1,at=0,adj=1)
mtext(text=". Fico Score: 737-785",side=1,line=1,col="green",las=1,padj=2,at=0,adj=1)
mtext(text=". Fico Score: 785-832",side=1,line=1,col="blue",las=1,padj=3,at=0,adj=1)
dev.copy2pdf(file="test.pdf")

summary(lm(loansData_642_689$Interest.Rate ~ loansData_642_689$Monthly.Income))
summary(lm(loansData_642_689$Interest.Rate ~ loansData_642_689$Amount.Requested))
summary(lm(loansData_642_689$Interest.Rate ~ loansData_642_689$Debt.To.Income))
summary(lm(loansData_642_689$Interest.Rate ~ loansData_642_689$Open.CREDIT.Lines))
summary(lm(loansData_642_689$Interest.Rate ~ loansData_642_689$Revolving.CREDIT.Balance))
summary(lm(loansData_642_689$Interest.Rate ~ loansData_642_689$Inquiries.in.the.Last.6.Months))
summary(lm(loansData_642_689$Interest.Rate ~ relevel(as.factor(loansData_642_689$State),ref="CA")))
summary(lm(loansData_642_689$Interest.Rate ~ as.factor(loansData_642_689$Employment.Length)))
summary(lm(loansData_642_689$Interest.Rate ~ as.factor(loansData_642_689$Loan.Purpose)))
summary(lm(loansData_642_689$Interest.Rate ~ as.factor(loansData_642_689$Loan.Length)))

summary(lm(loansData_689_737$Interest.Rate ~ loansData_689_737$Monthly.Income))
summary(lm(loansData_689_737$Interest.Rate ~ loansData_689_737$Amount.Requested))
summary(lm(loansData_689_737$Interest.Rate ~ loansData_689_737$Debt.To.Income))
summary(lm(loansData_689_737$Interest.Rate ~ loansData_689_737$Open.CREDIT.Lines))
summary(lm(loansData_689_737$Interest.Rate ~ loansData_689_737$Revolving.CREDIT.Balance))
summary(lm(loansData_689_737$Interest.Rate ~ loansData_689_737$Inquiries.in.the.Last.6.Months))
summary(lm(loansData_689_737$Interest.Rate ~ relevel(as.factor(loansData_689_737$State),ref="CA")))
summary(lm(loansData_689_737$Interest.Rate ~ as.factor(loansData_689_737$Employment.Length)))
summary(lm(loansData_689_737$Interest.Rate ~ as.factor(loansData_689_737$Loan.Purpose)))
summary(lm(loansData_689_737$Interest.Rate ~ as.factor(loansData_689_737$Loan.Length)))


summary(lm(loansData_737_785$Interest.Rate ~ loansData_737_785$Monthly.Income))
summary(lm(loansData_737_785$Interest.Rate ~ loansData_737_785$Amount.Requested))
summary(lm(loansData_737_785$Interest.Rate ~ loansData_737_785$Debt.To.Income))
summary(lm(loansData_737_785$Interest.Rate ~ loansData_737_785$Open.CREDIT.Lines))
summary(lm(loansData_737_785$Interest.Rate ~ loansData_737_785$Revolving.CREDIT.Balance))
summary(lm(loansData_737_785$Interest.Rate ~ loansData_737_785$Inquiries.in.the.Last.6.Months))
summary(lm(loansData_737_785$Interest.Rate ~ relevel(as.factor(loansData_737_785$State),ref="CA")))
summary(lm(loansData_737_785$Interest.Rate ~ as.factor(loansData_737_785$Employment.Length)))
summary(lm(loansData_737_785$Interest.Rate ~ as.factor(loansData_737_785$Loan.Purpose)))
summary(lm(loansData_737_785$Interest.Rate ~ as.factor(loansData_737_785$Loan.Length)))

summary(lm(loansData_785_832$Interest.Rate ~ loansData_785_832$Monthly.Income))
summary(lm(loansData_785_832$Interest.Rate ~ loansData_785_832$Amount.Requested))
summary(lm(loansData_785_832$Interest.Rate ~ loansData_785_832$Debt.To.Income))
summary(lm(loansData_785_832$Interest.Rate ~ loansData_785_832$Open.CREDIT.Lines))
summary(lm(loansData_785_832$Interest.Rate ~ loansData_785_832$Revolving.CREDIT.Balance))
summary(lm(loansData_785_832$Interest.Rate ~ loansData_785_832$Inquiries.in.the.Last.6.Months))
summary(lm(loansData_785_832$Interest.Rate ~ relevel(as.factor(loansData_785_832$State),ref="CA")))
summary(lm(loansData_785_832$Interest.Rate ~ as.factor(loansData_785_832$Employment.Length)))
summary(lm(loansData_785_832$Interest.Rate ~ as.factor(loansData_785_832$Loan.Purpose)))
summary(lm(loansData_785_832$Interest.Rate ~ as.factor(loansData_785_832$Loan.Length)))

summary(lm(loansData$Interest.Rate ~ loansData$Inquiries.in.the.Last.6.Months + as.factor(loansData$Loan.Length) + as.factor(loansData$FICO_4_ranges)))
confint(lm(loansData$Interest.Rate ~ loansData$Inquiries.in.the.Last.6.Months + as.factor(loansData$Loan.Length) + as.factor(loansData$FICO_4_ranges)))


### Not Used anymore

plot(loansData$Debt.To.Income.Ratio,loansData$Interest.Rate,pch=19,col=loansData$FICO_4_ranges,type="p")
plot(1:10,type="n",xaxt="n",yaxt="n")
legend(1,10,col=unique(loansData$FICO_4_ranges),legend=unique(loansData$FICO_4_ranges),pch=19)

coplot(loansData$Interest.Rate ~ loansData$Open.CREDIT.Lines |loansData$FICO_4_ranges, pch=19,columns=4,xlab="Debt To Income", ylab="Interest Rate")
