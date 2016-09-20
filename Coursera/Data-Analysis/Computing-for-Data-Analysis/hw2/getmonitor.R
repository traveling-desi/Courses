getmonitor <- function(id, directory, summarize = FALSE) {
	id <- as.character(id)
	if(nchar(id)==1) {
		id <- paste("00",id,sep="")
	} else if(nchar(id)==2) {
		id <- paste("0",id,sep="")
	}
	new_dir <- paste(directory,"/",id,".csv",sep="")
	data <- read.csv(file = new_dir, header = TRUE)
	if (summarize == TRUE) {
		print(summary(data))
	}
	return(data)
}