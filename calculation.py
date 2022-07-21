from calendar import month_abbr
import datetime as dt
from functools import total_ordering
from lib2to3.pytree import convert
from os import lseek
from time import time_ns
import pandas as pd
from sqlite3 import Date
from wsgiref import validate
from xmlrpc.client import DateTime
import numpy

#max weekly hours
maxwh=15
#max total hours
maxth=126
#max date range
maxdr = 59

total_hours = 0

class Req():
    #max weekly hours
    maxwh=15
    #max total hours
    maxth=126
    #max date range
    maxdr = 59

    total_hours = 0

    #time function
    def calcwh(start, lunchstart, lunchfinish, finish):
        start1 = Req.convert(start)
        finish1 = Req.convert(finish)
        lunchstart1 = Req.convert(lunchstart)
        lunchfinish1 = Req.convert(lunchfinish)
        total_day_hours = Req.calctd(start1, finish1)
        lunch_hours = Req.calcltd(lunchstart1, lunchfinish1)
        work_hours = total_day_hours - lunch_hours
        Req.total_hours += work_hours

    def totalhours():
        temp = Req.total_hours
        Req.total_hours == 0
        #print(temp)
        print (Req.total_hours)

    def calctd(t1, t2):
        hours = 12 - t1[0] + t2[0]
        if t2[1]<t1[1]:
            hours = hours - 1
            if t2[1] + t1[1] > 60:
                min = t2[1] + t1[1] - 60
                hours = hours + min/60
            if t2[1] + t1[1] == 60:
                hours = hours + 1

            if t2[1]>t1[1]:
                min = t2[1]-t1[1]
                hours = hours + min/60
        else:
            min = t2[1] + t1[1]
            hours = hours + min/60
        return (hours)
    
    def calcltd(t1, t2):
        hours = t2[0] - t1[0]
        if t2[1]<t1[1]:
            hours = hours - 1
            if t2[1] + t1[1] > 60:
                min = t2[1] + t1[1] - 60
                hours = hours + min/60
            if t2[1] + t1[1] == 60:
                hours = hours + 1

            if t2[1]>t1[1]:
                min = t2[1]-t1[1]
                hours = hours + min/60
        else:
            min = t2[1] + t1[1]
            hours = hours + min/60
        return (hours)

    def convert(time):
        dt1 = time.split(':')
        dt1[0] = int(dt1[0])
        dt1[1] = int(dt1[1])
        dt1[0] = Req.validatehour(dt1[0])
        Req.validateminutes(dt1[1])
        dt1[0] = int(dt1[0])
        dt1[1] = int(dt1[1])
        return (dt1)
    
    #date functions
    def datecomp(year, month, day):
        date = [0,0,0]
        date[0] = int(year)
        date[1] = int(month)
        date[2] = int(day)
        return date

    def datediff(date1,date2):
        d0 = dt.date(date1[0], date1[1], date1[2])
        d1 = dt.date(date2[0], date2[1], date2[2])
        delta = d1 - d0
        return(delta.days)   
    
    def calcweeks(days):
        if days%7 > 0:
            weeks = days//7 + 1
            print(weeks)
        if days%7 == 0:
            weeks = days/7
            print(weeks)

    def dayinweek(date1):
        return (date1.strftime('%A'))

    def sdayinweek(date1):
        return (date1.strftime('%a'))

    def findday(date, day):
        strdate = Req.arrtodt(date)
        for i in range(0,6):
            if Req.dayinweek(strdate+dt.timedelta(days=i)) == day or Req.sdayinweek(strdate+dt.timedelta(days=i)) == day : 
                return (Req.dttostr(strdate+dt.timedelta(days=i)))

    def arrtodt(date):
        return dt.datetime(date[0], date[1], date[2])

    def dttostr(datetime):
        return dt.datetime.strftime(datetime, "%Y-%m-%d")

    def datearrtostr(date):
        return dt.datetime.strftime(dt.datetime(date[0], date[1], date[2]), "%Y-%m-%d")

    def datetimearrtostr(date, time):
        time1 = Req.splittime(time)
        return dt.datetime.strftime(dt.datetime(date[0], date[1], date[2], time1[0], time1[1]), "%Y-%m-%d %H:%M")

    def splittime(time):
        time1 = time.split(":")
        time1[0] = int(time1[0])
        time1[1] = int(time1[1])
        return(time1)

    def generate(startdate, enddate):
        periods = pd.date_range(start=startdate, end = enddate, freq="7D", inclusive="both")
        periods2 = numpy.array(periods)
        times=[]
        for i in range(len(periods2)):
            period = str(periods[i])
            times.append(period.split("T"))
        print (times[0])

    #time validation
    def validatehour(num):
        if num > 23:
            return "Error"
        return num

    def validateminutes(num):
        if num > 59:
            print ("Minutes is over 59 which is invalid ")
        return num
    
    def validateweeklyhours(wh):
        if wh > maxwh:
            print("Raise Error")
        return wh

    def validateworkinghours(th):
        if th > maxth:
            print("Raise error")
        return th

    def validatedatediff(date1, date2):
        if Req.datediff(date1, date2) > maxdr:
            print("Raise Error")
        return Req.datediff(date1, date2)    

    def validatedate(date):
        dt.datetime(year=date[0], month=date[1], day=date[2])

    def test():

        #Req.calcwh("9:00","1:00","2:00","6:00")
        #Req.calcwh("9:00","13:00","14:00","18:00")
        #Req.totalhours()
        #Req.calcweeks(50)
        #Req.datetimearrtostr([2022,7,21],"13:30")
        #Req.datearrtostr([2022,7,21])
        Req.generate(Req.findday([2022,7,21],"Sun"), "2022-8-20")
        return
