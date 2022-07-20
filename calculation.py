from calendar import month_abbr
import datetime as dt
from functools import total_ordering
from lib2to3.pytree import convert
from os import lseek
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
        dt1[0] = Req.validateh(dt1[0])
        Req.validatem(dt1[1])
        dt1[0] = int(dt1[0])
        dt1[1] = int(dt1[1])
        return (dt1)
    
    #date functions
    def datecomp(year, month, day):
        date = []
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

    def findday(date):
        today = dt.datetime(date[0], date[1], date[2])
        print (today.strftime('%A'))


    #time validation
    def validateh(num):
        if num > 12:
            num = num-12
            return num
        return num

    def validatem(num):
        if num > 59:
            print ("Minutes is over 59 which is invalid ")
        return num
    
    def validatewh(wh):
        if wh > 126:
            print("Raise error")
        return wh

    def validatedatediff(date1, date2):
        if Req.datediff(date1, date2) > 59:
            print("Raise Error")
        return Req.datediff(date1, date2)    

    def validatedate(date):
        dt.datetime(year=date[0], month=date[1], day=date[2])

    def test():

        #Req.calcwh("9:00","1:00","2:00","6:00")
        #Req.calcwh("9:00","13:00","14:00","18:00")
        #Req.totalhours()
        Req.calcweeks(50)
        return

Req.test()
