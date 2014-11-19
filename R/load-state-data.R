
library(devtools)
install_github("mmadsen/mmadsenr")
library(mmadsenr)


#setwd("/Volumes/Macintosh HD/Users/clipo/spatialTransmission/R")
#setwd("../data/")
#file_list <- list.files("../data/namesbystate/",pattern="\\.TXT$", full.names=TRUE)

file_list <- list_files_for_data_path(directory = "spatialTransmission/data/namesbystate", pattern="\\.TXT$")
for (file in file_list){
  # if the merged dataset doesn't exist, create it
  if (!exists("dataset")){
    dataset <- read.table(file, header=FALSE, sep=",", col.names=c("State","Sex","Year","Name","Count"))
  }
  # if the merged dataset does exist, append to it
  if (exists("dataset")){
    temp_dataset <-read.table(file, header=FALSE, sep=",", col.names=c("State","Sex","Year","Name","Count"))
    dataset<-rbind(dataset, temp_dataset)
    rm(temp_dataset)
  }
  
} 
