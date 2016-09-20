
agecount <- function(age = NULL) {	
	if (is.null(age)) {
		stop("No age Provided")
	} 
	setwd("/Users/sarpotd/Desktop/Coursera/Data Analysis/hw4/")
	homicides <- readLines("homicides.txt")
	str_to_search <- paste("",as.character(age),"year",sep = "( )+")
	#print(str_to_search)
	length(grep(str_to_search,homicides,ignore.case = TRUE))
}
