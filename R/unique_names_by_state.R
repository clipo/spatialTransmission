
plot_graphs <- function(filename, title) {
  states <- unique(dataset$State)
  
  par(mfrow=c(10,5), mar=c(2,2,2,2))
  for (st in states) { 
    statedata <- data.frame()
    first <- 1910
    last <-2013
    for (year in seq(first,last)) {
      yeardata <- subset(dataset,Year==year & State==st,select=c(Name,Count))
      number<-length(unique(yeardata$Name))
      total<-sum(yeardata$Count)
      #pop <- subset(shiller.other.data, Year==year & State==st, select=U.S.Population, row.names=FALSE)
      if (year==first) {
        change<-0
        change_in_uniques <- 0
        previous_list <- yeardata$Name
        correct <- 0
        oldval <- 0
      } else {
        change <- number-oldval
        change_in_uniques = length(setdiff(previous_list, unique(yeardata$Name) ))
        correct <- change_in_uniques/total
      }
      newRow <- data.frame(Year=year, UniqueNames=number,  Change=change/total,
                         Change_In_Uniques=change_in_uniques, 
                         ChangePopCorrectedTotal=correct)
      statedata<-rbind(statedata,newRow)
    }
    
    plot.ts(statedata$UniqueNames)
    plot(statedata$Year,statedata$UniqueNames,type='l',main=st, col='black',xlab="Year",ylab="Number of Unique Names")
    par(new=T)
    plot(statedata$Year,statedata$ChangePopCorrectedTotal,type="l",col="blue",xaxt="n",yaxt="n",xlab="",ylab="")
    axis(4)
  
  }
}

plot_graphs(dataset, "Innovation in Baby Names by State")
  