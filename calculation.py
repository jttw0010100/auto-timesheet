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
        total_day_hours = convert(start,finish)
        lunch_hours = convert(lunchstart,lunchfinish)
        #work_hours = total_day_hours - lunch_hours
        return Req.calctd(start,finish)
        
    def calctd(t1, t2):
        hours = 0
        hours = (12-t1[0])+t2[0]
        if t2[1]<t1[1]:
            hours = hours - 1
            if t2[1] + t1[1] > 60:
                min = t2[1] + t1[1] - 60
                hours = hours + min * 60
            if t2[1] + t1[1] == 60:
                hours = hours + 1
            else:
                min = t2[1] + t1[1]
                hours = hours + min * 60

    def convert(time, time2):
        dt1 = []
        dt1 = time.split(':')
        dt2 = []
        dt2 = time2.split(':')
        dt1[0] = int(dt1[0])
        dt1[1] = int(dt1[1])
        dt2[0] = int(dt1[0])
        dt1[1] = int(dt1[1])
        

Req.calctd([12,00],[23,00])