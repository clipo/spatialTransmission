import csv
import argparse
import logging as logger
import sys
import os
import sqlite3 as sql

### Script to suck up babyname data to sqlite and do some basic calculations

class aggregateData():
    def __init__(self):
        self.inputfile = ""
        self.minyear =0
        self.maxyear =0
        self.names = {}
        self.stateNumber=0
        self.nameNumber=0
        try:
            self.conn = sql.connect('babynames.sqlite')
            self.curr = self.conn.cursor()
        except sql.Error, e:
            print "Error %s: " % e.args[0]
            sys.exit(1)

    def openFiles(self, directory):

        for file in os.listdir(directory):
            print file
            if file.endswith(".TXT" ) and file<>None:
                try:
                    logger.debug("trying to open: %s ", file)
                    filename = open(directory+"/"+file, 'r')
                    self.insertState(file[0:-4])
                    self.stateNumber += 1
                    reader = csv.reader(filename, delimiter=',', quotechar='|')
                    for row in reader:
                        #print row
                        self.nameNumber += 1
                        row = map(str, row)
                        state = row[0]
                        sex = row[1]
                        year= row[2]
                        name=row[3]
                        count=row[4]
                        #args =( self.nameNumber, state,year,name,sex,count,0.0)
                        #self.curr.execute("INSERT INTO names VALUES(?,?,?,?,?,?,?)", args)
                        #self.conn.commit
                except csv.Error as e:
                    logger.error("Cannot open %s. Error: %s", file, e)
                    sys.exit('file %s does not open: %s') % ( file, e)

    def insertState(self, state):
        if state <> None:
            args = (self.stateNumber, state)
            print args
            self.curr = self.conn.cursor()
            self.curr.execute("Insert INTO states VALUES (?,?)",args)
            self.conn.commit

    def updatePercentages(self):
        self.curr = self.conn.cursor()
        self.curr.execute("select * from states")
        rows = self.curr.fetchall()
        print rows
        for row in rows:
            state = row[1]
            for y in range(1910,2013,1):
                args=(state,y)
                self.curr.execute("select sum(count) from names where state=? and year=?",args)
                count=self.curr.fetchall()
                print count

    def parse_arguments(self):
        parser = argparse.ArgumentParser(description='Suck up babyname data in to sqlite database')
        parser.add_argument('--debug', '-d', default=None, help='Sets the DEBUG flag')
        try:
            self.args = vars(parser.parse_args())
        except IOError, msg:
            parser.error(str(msg))
            sys.exit()
        return self.args

if __name__ == "__main__":
    babynames = aggregateData()
    args = babynames.parse_arguments()
    babynames.openFiles(directory="../data/namesbystate")
    babynames.updatePercentages()