complete <- function(directory, fid = 1:332) {
dfrm <- data.frame(id=numeric(0),nobs=character(0))	
for (i in fid) {
		tid <- as.character(i)
		if(nchar(tid)==1) {
			tid <- paste("00",tid,sep="")
		} else if(nchar(tid)==2) {
			tid <- paste("0",tid,sep="")
		}
		#print(tid)
		new_dir <- paste(directory,"/",tid,".csv",sep="")
		#print(new_dir)
		data <- na.omit(read.csv(file = new_dir, header = TRUE))
		nob_s=nrow(data)
		#print(nob_s)
		newrow <- data.frame(id=as.integer(tid),nobs=nob_s)
		#print(newrow)
		dfrm <- rbind(dfrm,newrow)
		#print(dfrm)
	}
	print(dfrm)
}