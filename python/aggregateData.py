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
        self.conn= None
        self.curr= None
        self.states=['AK','AL','AR','AZ',
                      'CA','CO','CT','DC','DE',
                      'FL','GA','HI','IA','ID',
                      'IL','IN','KS','KY','LA',
                      'MA','MD','ME','MI','MN',
                      'MO','MS','MT','NC','ND',
                      'NE','NH','NJ','NM','NV',
                      'NY','OH','OK','OR','PA',
                      'RI','SC','SD','TN','TX',
                      'UT','VA','VT','WA','WI',
                      'WV','WY']
        try:
            self.conn = sql.connect('babynames.sqlite')
            self.curr = self.conn.cursor()
            self.conn.row_factory = sql.Row
        except sql.Error, e:
            print "Error %s: " % e.args[0]
            sys.exit(1)


    def openFiles(self, directory):

        self.curr.execute("DROP TABLE IF EXISTS names")
        self.curr.execute("CREATE TABLE names (id INTEGER PRIMARY KEY Autoincrement  NOT NULL  UNIQUE , state TEXT,year INTEGER, name TEXT, sex TEXT, count INTEGER, percent NUMERIC)")
        for state in self.states:
            statefile=state+".TXT"
            try:
                logger.debug("trying to open: %s ", file)
                filename = open(directory+"/"+statefile, 'r')
                reader = csv.reader(filename, delimiter=',', quotechar='|')
                for row in reader:
                    self.nameNumber += 1
                    row = map(str, row)
                    state = row[0]
                    sex = row[1]
                    year= row[2]
                    name=row[3]
                    count=row[4]
                    args =( self.nameNumber, state,year,name,sex,count,0.0)
                    self.curr.execute("INSERT INTO names VALUES(?,?,?,?,?,?,?)", args)
            except csv.Error as e:
                    logger.error("Cannot open %s. Error: %s", file, e)
                    sys.exit('file %s does not open: %s') % ( file, e)
            self.conn.commit()

    def insertState(self, state):
        if self.stateNumber <> None:
            args = (self.stateNumber, state)
            print args
            self.curr = self.conn.cursor()
            self.curr.execute("Insert INTO states VALUES (?,?)",args)
            self.conn.commit()

    def updatePercentages(self):
        for state in self.states:
            for y in range(1910,2013,1):
                args=(state,y)
                self.curr.execute("select sum(count) from names where state=? and year=?",args)
                row=self.curr.fetchall()
                stateyeartotal = row[0]
                #print "total: ", row
                #exit()
                self.curr.execute("select * from names where state=? and year=?",args)
                rows=self.curr.fetchall()

                for row in rows:
                    percent=row["count"]/stateyeartotal
                    args=(percent,row["id"])
                    self.curr.execute("update names set percent=? where id=?",args)

    def createYearFiles(self):
        for y in range(1910,2013,1):
            ## openfile for year
            filename=str(y)+".TXT"
            writer=open(filename,"w")
            ## create header
            self.curr.execute("select name from names where year=?",y)
            names=self.curr.fetchall()
            with writer:
                writer.write("State\t")
            for n in names:
                with writer:
                    writer.write(names+"\t")
            stateHash = {}
            for state in self.states:
                row=self.curr.fetchall()
                stateyeartotal = row[0]
                self.curr.execute("select * from names where state=? and year=?",args)
                rows=self.curr.fetchall()
                for row in rows:
                    percent=row["count"]/stateyeartotal
                    args=(percent,row["id"])
                    self.curr.execute("update names set percent=? where id=?",args)

    def test(self):
        self.curr.execute("DROP TABLE IF EXISTS namestest")
        self.conn.commit()
        self.curr.execute("CREATE TABLE namestest (id INTEGER PRIMARY KEY Autoincrement  NOT NULL  UNIQUE , state TEXT,year INTEGER, name TEXT, sex TEXT, count INTEGER, percent NUMERIC)")
        args=( (1,"CA",1910,"Bob","M",100,0.0),
               (2,"WA",1911,"Bobby","F",200,0.0),
               (3,"OR",1912,"Robert","M",300,0.0))
        self.curr.executemany("INSERT INTO namestest VALUES (?,?,?,?,?,?,?)", args)
        self.conn.commit()
        self.curr.execute("select * from namestest")
        rows = self.curr.fetchall()
        rcount =0
        for row in rows:
            #print row
            rcount +=1
        if rcount <> 3:
            logger.error("Sqlite database failure.")
            sys.exit('problem with sqlite database. Test failed')

        self.curr.execute("DROP TABLE IF EXISTS namestest")

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
    #babynames.test()