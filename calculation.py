import datetime as dt
from lib2to3.pytree import convert
from os import lseek
from sqlite3 import Date
from xmlrpc.client import DateTime

class Req():
    #max weekly hours
    maxwh=15
    #max total hours
    maxth=126
    #max date range
    maxdr = 59

    total_hours = 0

    def calcwh(start, lunchstart, lunchfinish, finish):
        start1 = Req.convert(start)
        finish1 = Req.convert(finish)
        lunchstart1 = Req.convert(lunchstart)
        lunchfinish1 = Req.convert(lunchfinish)
        total_day_hours = Req.calctd(start1, finish1)
        lunch_hours = Req.calcltd(lunchstart1, lunchfinish1)
        print (total_day_hours-lunch_hours)
        
    def calctd(t1, t2):
        hours = 0
        hours = (12-t1[0]) + t2[0]
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
        hours = 0
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
        dt1 = []
        dt1 = time.split(':')
        dt1[0] = int(dt1[0])
        dt1[1] = int(dt1[1])
        return(dt1)

Req.calcwh("9:45","1:00","2:00","6:00")