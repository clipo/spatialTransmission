
library(devtools)
#install_github("mmadsen/mmadsenr")
library(mmadsenr)

library(foreign)
#setwd("/Volumes/Macintosh HD/Users/clipo/spatialTransmission/R")

for (y in seq(1911,2013)) {
  filename <- paste0("../data/shapefiles/", y, "-continuity-minmax-by-weight.dbf")
  dbfdata <- read.dbf(filename, as.is = TRUE)
  dbfdata$Date <- paste0(y,"/01/01")
  ## overwrite the file with this new copy
  write.dbf(dbfdata, filename)
}