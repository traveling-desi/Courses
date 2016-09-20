best <- function(state, outcome) {
	
	setwd("/Users/sarpotd/Desktop/Coursera/Data Analysis/hw3")
	outcome_file <- read.csv("ProgAssignment3-data/outcome-of-care-measures.csv", colClasses = "character")
	
	state_names <- unique(outcome_file$State)
	outcome_names <- c("heart attack", "heart failure", "pneumonia")
	if(!any(state_names == state)) {
		stop("invalid state")
		} else if (!any(outcome_names == outcome)) {
		stop("invalid outcome")
		} else {
			if (outcome == "heart attack") {
				outcome_file_subset <- subset(outcome_file,subset=(outcome_file$State==state), sel=c(Hospital.Name, Hospital.30.Day.Death..Mortality..Rates.from.Heart.Attack))		
			} else if (outcome == "heart failure") {
				outcome_file_subset <- subset(outcome_file,subset=(outcome_file$State==state), sel=c(Hospital.Name, Hospital.30.Day.Death..Mortality..Rates.from.Heart.Failure))				} else if (outcome == "pneumonia") {
				outcome_file_subset <- subset(outcome_file,subset=(outcome_file$State==state), sel=c(Hospital.Name, Hospital.30.Day.Death..Mortality..Rates.from.Pneumonia))					}
			#print("Here")
			#print(head(outcome_file_subset))
			colnames(outcome_file_subset) <- c("H.name", "H.outcome")
			#print(head(outcome_file_subset))			
			outcome_file_subset[,"H.outcome"] <- as.numeric(outcome_file_subset[,"H.outcome"])
			outcome_file_subset <- na.omit(outcome_file_subset)
			#print(head(outcome_file_subset))			
			outcome_file_subset <- outcome_file_subset[order(outcome_file_subset$H.outcome),]
			print(outcome_file_subset[1,1])			
		}
}