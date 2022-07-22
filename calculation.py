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
import PySimpleGUI as sg
import socket

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
        return (Req.total_hours)

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
        date = [year, month, day]
        return date

    def datediff(date1,date2):
        d0 = Req.strtodt(date1)
        d1 = Req.strtodt(date2)
        delta = d1 - d0
        return(delta.days)   
    
    def calcweeks(days):
        if days%7 > 0:
            weeks = days//7 + 1
            return(weeks)
        if days%7 == 0:
            weeks = days/7
            return(weeks)

    def dayinweek(date1):
        return (date1.strftime('%A'))

    def sdayinweek(date1):
        return (date1.strftime('%a'))

    def findday(date, day):
        strdate = Req.strtodt(date)
        for i in range(0,6):
            if Req.dayinweek(strdate+dt.timedelta(days=i)) == day or Req.sdayinweek(strdate+dt.timedelta(days=i)) == day : 
                return (Req.dttostr(strdate+dt.timedelta(days=i)))

    def listtodt(date):
        return dt.datetime(int(date[0]), int(date[1]), int(date[2]))

    def listtostr(date):
        return dt.datetime.strftime(dt.datetime(date[0], date[1], date[2]),"%Y-%m-%d")

    def strtodt(date):
        return dt.datetime.strptime(date, "%Y-%m-%d %H:%M")    
    
    def dttostr(datetime):
        return dt.datetime.strftime(datetime, "%Y-%m-%d  %H:%M")

    def datelisttostr(date):
        return dt.datetime.strftime(dt.datetime(date[0], date[1], date[2]), "%Y-%m-%d")

    def datetimelisttostr(date, time):
        time1 = Req.splittime(time)
        return dt.datetime.strftime(dt.datetime(date[0], date[1], date[2], time1[0], time1[1]), "%Y-%m-%d %H:%M")
    
    def addtimetodate(date, hour, minute):
        return dt.date.strftime(dt.datetime(date[0], date[1], date[2], hour, minute), "%Y-%m-%d %H:%M")

    def splittime(time):
        time1 = time.split(":")
        time1[0] = int(time1[0])
        time1[1] = int(time1[1])
        return(time1)

    def generate(startdate, enddate, frequency):
        enddate = Req.listtodt(enddate)
        periods = pd.date_range(start=startdate, end = enddate, freq=frequency, inclusive="both")
        periods2 = numpy.array(periods)
        times=[]
        for i in range(len(periods2)):
            period = str(periods[0])
            times.append(period)
        return (times)
        
    
    #txt = "2022-07-03T13:00:00.000000000"
    #print (txt.split("T"))

    #time validation
    def validatehour(num):
        if num > 23:
            sg.Popup('Oops!', str(num) + ' is not a valid time')
            quit()
        return num

    def validateminutes(num):
        if num > 59:
            sg.Popup('Oops!', str(num) + ' is not a valid time')
            quit()
        return num
    
    def validateweeklyhours(wh):
        if wh > maxwh:
            sg.Popup('Oops!', 'Maximum of ' + str(59) + ' total hours exceeded')
            quit()
        return wh

    def validateworkinghours(th):
        if th > maxth:
            sg.Popup('Oops!', 'Maximum of ' + str(59) + ' working hours exceeded')
            quit()
        return th

    def validatedatediff(date1, date2):
        if Req.datediff(date1, date2) > 59:
            sg.Popup('Oops!', 'Date range of ' + str(59) + ' exceeded')
            quit()
        return Req.datediff(date1, date2)    

    def validatedate(date):
        dt.datetime(year=date[0], month=date[1], day=date[2])

    def test():

        #Req.calcwh("9:00","1:00","2:00","6:00")
        #Req.calcwh("9:00","13:00","14:00","18:00")
        #Req.totalhours()
        #Req.calcweeks(50)
        #Req.validatedatediff([2022,1,1],[2022,12,20])
        #Req.datetimelisttostr([2022,7,21],"13:30")
        #Req.datelisttostr([2022,7,21])
        Req.generate(Req.findday("2022-7-21 00:00","Sun"), [2022,8,20], "7D")
        #Req.datecomp(2022,2,24)
        return

Req.test()