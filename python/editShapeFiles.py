__author__ = 'carllipo'
import datetime
#from mx import DateTime
from dbfpy import dbf

for y in range(1911,2014,1):
    file= "/Volumes/Macintosh HD/Users/carllipo/spatialTransmission/data/shapefiles/" + str(y) +"-continuity-minmax-by-weight.dbf"
    db = dbf.Dbf(file, new=False)
    db.addField(("Date_Of_Birth", "C",12))
    rec=db.newRecord()
    rec["Date_Of_Birth"]=str(y)+"/01/01"
    print rec["Date_Of_Birth"]
    db.close()