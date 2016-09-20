corr <- function(directory, threshold = 0) {
fid <- dir(directory)
new <- NA
for (i in fid) {
		tid <- as.character(i)
		if(nchar(tid)==1) {
			tid <- paste("00",tid,sep="")
		} else if(nchar(tid)==2) {
			tid <- paste("0",tid,sep="")
		}
		#print(tid)
		new_dir <- paste(directory,"/",tid,sep="")
		#print(new_dir)
		data <- na.omit(read.csv(file = new_dir, header = TRUE))
		nob_s=nrow(data)
		if (nob_s > threshold){
			new <- c(new,cor(data$sulfate,data$nitrate))
		}
	}
	new <- new[!is.na(new)]
	return(new)
}