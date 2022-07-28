from calendar import month_abbr
from csv import reader
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
from see_excel import ReadExcel

class Req():    

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
    def datecomp2(year, month, day):
        date = [year, month, day]
        return date

    def datediff(date1,date2):
        d0 = Req.strtodt(date1)
        d1 = Req.strtodt(date2)
        delta = d1 - d0
        return(delta.days)  
     
    def listdatediff(date1,date2):
        d0 = Req.listtodt(date1)
        d1 = Req.listtodt(date2)
        delta = d1 - d0
        return(delta.days)  
    
    def find_workinghours(time1, time2):
        t1 = dt.datetime.strptime(time1,"%Y-%m-%d %H:%M:%S")
        t2 = dt.datetime.strptime(time2,"%Y-%m-%d %H:%M:%S")
        delta = t2 - t1
        """
        print (t1)
        print (t2)
        print(delta)
        """
        return (int(delta.total_seconds()/60/60))

    def calcweeks(days):
            weeks = days/7
            return(weeks)

    def dayinweek(date1):
        return (date1.strftime('%A'))

    def sdayinweek(date1):
        return (date1.strftime('%a'))

    def findday(date, day):
        strdate = Req.strtodt(date)

        #enable below if statement if startdate does not include first workday
        #if Req.dayinweek(strdate) == day or Req.sdayinweek(strdate) == day : 
            #return (Req.dttostr(strdate+dt.timedelta(days=7)))

        for i in range(0,7):
            if Req.dayinweek(strdate+dt.timedelta(days=i)) == day or Req.sdayinweek(strdate+dt.timedelta(days=i)) == day : 
                return (Req.dttostr(strdate+dt.timedelta(days=i)))

    def listtodt(date):
        return dt.datetime(int(date[0]), int(date[1]), int(date[2]))
    
    def listtostrdate(date):
        return str(date[0]) + "-" + str(date[1])+ "-" + str(date[2])

    def listtostr(date):
        return dt.datetime.strftime(dt.datetime(date[0], date[1], date[2]),"%Y-%m-%d")

    def strtodt(date):
        return dt.datetime.strptime(date, "%Y-%m-%d %H:%M")    
    
    def dttostr(datetime):
        return dt.datetime.strftime(datetime, "%Y-%m-%d  %H:%M")
    
    def strdatetodt(date):
        return dt.datetime.strptime(date,"%Y-%m-%d")    

    def strdatetostr(date,hour, minute):
        if hour<10:
            hour= "0"+ str(int(hour))
        if minute<10:
            minute = "0"+str(int(minute))
        date = date + " " + str(hour) + ":" + str(minute)
        return (date)
    
    def timetostr(hour, minute):
        if hour<10:
            hour= "0"+ str(int(hour))
        if minute<10:
            minute = "0"+str(int(minute))
        date = str(hour) + ":" + str(minute) + ":00"
        return (date)

    def datelisttostr(date):
        return dt.datetime.strftime(dt.datetime(date[0], date[1], date[2]), "%Y-%m-%d")

    def datetimelisttostr(date, time):
        time1 = Req.splittime(time)
        return dt.datetime.strftime(dt.datetime(date[0], date[1], date[2], time1[0], time1[1]), "%Y-%m-%d %H:%M")
    
    def addtimetodate(date, hour, minute):
        return dt.date.strftime(dt.datetime(date[0], date[1], date[2], hour, minute), "%Y-%m-%d %H:%M")

    def addtime(date, timetoadd):
        date2 = dt.datetime.strptime(date, "%Y-%m-%d %H:%M")
        timetoadd2 = timetoadd*60
        date3 = date2+dt.timedelta(minutes = timetoadd2)
        return str(date3)
    
    def gethourminute(time):
        txt = time
        txts = txt.split(" ")
        return txts[1]

    def getdate(time):
        txt = time
        txts = txt.split(" ")
        return txts[0]

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
            period = str(periods[i])
            times.append(period)
        return times
    
    def generate2(startdate, enddate, frequency):
        enddate = Req.listtodt(enddate)
        periods = pd.date_range(start=startdate, end = enddate, freq=frequency, inclusive="both")
        periods2 = numpy.array(periods)
        times=[]
        for i in range(len(periods2)):
            period = str(periods[i])
            periods3 = period.split(" ")
            times.append(periods3[0])
        return times


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
        if wh > ReadExcel.total_weekly_hour_limit():
            limit = ReadExcel.total_weekly_hour_limit()
            sg.Popup('Oops!', 'Maximum of ' + str(int(limit)) + ' total hours exceeded')
            return False

    def validateworkinghours(th):
        if th > ReadExcel.total_work_hours_limit():
            limit = ReadExcel.total_work_hours_limit()
            sg.Popup('Oops!', 'Maximum of ' + str(int(limit)) + ' working hours exceeded')
            return False
        if ReadExcel.total_weekly_hour_limit()>126:
            sg.Popup('Oops!', 'FEO maximum total hours is 126 hours')

    def validatedatediff(diff):
        if diff > ReadExcel.total_date_range_limit():
            limit = ReadExcel.total_date_range_limit()
            sg.Popup('Oops!', 'Date range of ' + str(int(limit)) + ' days exceeded')
            return False  

    def validatedate(inputdate):
        year, month, day = inputdate.split('-')
        try:
            dt.datetime(int(year), int(month), int(day))
        except ValueError:
            return False
        return True
    
    #def validatedate(date):
       #dt.datetime(year=date[0], month=date[1], day=date[2])
