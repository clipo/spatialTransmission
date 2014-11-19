library(reshape)

library(devtools)
install_github("mmadsen/mmadsenr")
library(mmadsenr)


for (year in seq(1910,2013)) {
  yeardata <- subset(dataset,Year==year,select=c(State,Name,Count))
  d.m <- melt(yeardata)
  out <- cast(d.m, State ~ Name, sum)
  filename <- paste0("./data/namesbyyear/", year, ".txt")
  write.table(out, file=filename, sep="\t")
}