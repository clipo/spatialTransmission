
library(reshape)
library(datasets)
library(devtools)
#install_github("mmadsen/mmadsenr")
library(mmadsenr)
library(nutshell)
data(toxins.and.cancer)
usdata <- data.frame()
first <- 1910
last <-2013
for (year in seq(first,last)) {
  yeardata <- subset(dataset,Year==year,select=c(Name,Count))
  number<-length(unique(yeardata$Name))
  total<-sum(yeardata$Count)
  pop <- subset(shiller.other.data, Year==year, select=U.S.Population, row.names=FALSE)
  if (year==first) {
    change<-0
    change_in_uniques <- 0
    previous_list <- yeardata$Name
    correct <- 0
  } else {
    change <- number-oldval
    change_in_uniques = length(setdiff(previous_list, unique(yeardata$Name) ))
    correct <- change_in_uniques/total
  }
  newRow <- data.frame(Year=year, UniqueNames=number,  Change=change/total,
                       Change_In_Uniques=change_in_uniques, 
                       ChangePopCorrectedTotal=correct)
  usdata<-rbind(usdata,newRow)
}
par(mar=c(5, 12, 4, 4) + 0.1)
plot(usdata$Year,usdata$UniqueNames,type='l',col='black',xlab="Year",ylab="Number of Unique Names")
par(new=T)
plot(usdata$Year,usdata$ChangePopCorrectedTotal,type="l",col="blue",xaxt="n",yaxt="n",xlab="",ylab="")
axis(4)

mtext("New Names",side=4,line=3)
legend("topleft",bty = "n",col=c("red","blue"),lty=1,legend=c("Number of Unique Names","New Names Relative to Previous Year"))

### state by state analyses...
#for (st in state.abb) {  
#    statedata <- subset(dataset,State==st,select=c(State,Name,Count))
#    d.m <- melt(yeardata)
#    # first output by us total number 
#    out <- cast(d.m, State ~ Name, sum)
#}
