count <-  function(cause = NULL) {
	causes <- c("asphyxiation",  "blunt force",  "other",  "shooting",  "stabbing",  "unknown")
	#print(causes)	
	#print(cause)	
	if (is.null(cause)) {
		stop("No Cause Provided")
	} 
	if (!any(causes == cause)) {
		stop("Wrong Cause provided")
	}
	setwd("/Users/sarpotd/Desktop/Coursera/Data Analysis/hw4/")
	homicides <- readLines("homicides.txt")
	str_to_search <- paste("Cause:",cause,sep = " ")
	#print(str_to_search)
	length(grep(str_to_search,homicides,ignore.case = TRUE))
}
