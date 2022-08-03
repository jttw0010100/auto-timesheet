import exceledit 
import pandas as pd
import datetime as dt
import numpy
from see_excel import ReadExcel
from calculation import Req
import PySimpleGUI as sg
from openpyxl.styles import Border, Side
import openpyxl
import xlsxwriter
import socket
import glob
import os

class Temp():
    
    Statutory_Holidays = ReadExcel.get_public_holidays()
    Days_in_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    startdate = ReadExcel.find_start()
    enddate = ReadExcel.find_end()
    days = []
    publicholidays = []
    leftover = 0
    days = Req.generate2(Req.datelisttostr(startdate), enddate, "1D")
    days2 = Req.generate2(Req.datelisttostr(startdate), enddate, "1D")

    dayofweek1 = ReadExcel.dayofweek1()
    dayofweek2 = ReadExcel.dayofweek2()

    blacklist = []

    invalid = 0
    for day in days2:
        for holiday in Statutory_Holidays:
            if day == holiday:
                invalid = 0
                dayofweek = Req.dayinweek(Req.strdatetodt(day))
                if (dayofweek in Days_in_week):
                    Days_in_week.remove(dayofweek)
                    days.remove(holiday)
                    blacklist.append(dayofweek)
                    publicholidays.append(day)
                if dayofweek1 == dayofweek or dayofweek2 == dayofweek:
                    invalid = invalid + 1
    print(blacklist)

    if len(blacklist)>0:
        if dayofweek1 != blacklist[0] and dayofweek2 != blacklist[0]:
            if len(blacklist)>1:
                if dayofweek1 != blacklist[1] and dayofweek2 != blacklist[1]:
                    invalid = 0
            if len(blacklist)<=1:
                invalid = 0
    
    if invalid > 0:
        sg.Popup('The days in week you have chosen includes a public holiday. Public holidays: ', publicholidays, 'Please choose days from this list:', Days_in_week)
        quit()


    if dayofweek1 == "Saturday" or dayofweek2 == "Saturday":
        sg.Popup('Are you sure you want to work on Saturday? If so ignore this popup')


    #day 1 
    starttime = Req.addtimetodate(ReadExcel.find_start(), 9,0)
    lunchstart = Req.addtimetodate(ReadExcel.find_start(), 13,0)
    lunchend = Req.addtimetodate(ReadExcel.find_start(), 14,0)
    endtime = Req.addtimetodate(ReadExcel.find_start(),18,0)

    #day 2
    starttime2 = Req.addtimetodate(ReadExcel.find_start(), 10,0)
    lunchstart2 = Req.addtimetodate(ReadExcel.find_start(), 13,0)
    lunchend2 = Req.addtimetodate(ReadExcel.find_start(), 14,0)
    endtime2 = Req.addtimetodate(ReadExcel.find_start(),18,0)

    if (Req.strtodt(Req.findday(starttime,dayofweek1))) > (Req.strtodt(Req.findday(starttime,dayofweek2))):
        dayofweek1 = ReadExcel.dayofweek2()
        dayofweek2 = ReadExcel.dayofweek1()
    
    #day 1 generator
    genstart1d1 = Req.generate(Req.findday(starttime,dayofweek1), enddate,"7D")
    genlunch1d1 = Req.generate(Req.findday(lunchstart,dayofweek1), enddate, "7D")
    genlunch2d1 = Req.generate(Req.findday(lunchend,dayofweek1), enddate, "7D")
    genendd1 = Req.generate(Req.findday(endtime,dayofweek1), enddate, "7D")

    #day 2 generator
    genstart1d2 = Req.generate(Req.findday(starttime2,dayofweek2), enddate,"7D")
    genlunch1d2 = Req.generate(Req.findday(lunchstart2,dayofweek2), enddate, "7D")
    genlunch2d2 = Req.generate(Req.findday(lunchend2,dayofweek2), enddate, "7D")
    genendd2 = Req.generate(Req.findday(endtime2,dayofweek2), enddate, "7D")

    numofdates = len(genstart1d1) + len(genstart1d2)

    dates = []
    working_hours = []
    temp = []
    
    gd = pd.DataFrame(
                columns = ['Date','Day','Office Start', 'Lunch Start', 'Lunch End', 'Office End','Hours', 'Duty']
                )
    
    gd2 = pd.DataFrame(
        columns = ['Weeks', 'Date Range', 'Total Hours', 'FEO limit hours']
        )
    gd3 = pd.DataFrame(
        columns = ['Sum of total hours']
        )
    gd4 = pd.DataFrame(
        columns = ['Sum of total hours']
    )
    #enddate - startdate/7 * 15

    #compile dates(not needed)
    #for x in range(int(numofdates/4)):
        #dates.append(genstart3[x])
        #dates.append(genlunch1[x])
        #dates.append(genlunch2[x])
        #dates.append(genend[x]

    def compile(num,start,lunch1,lunch2,end):
        list=[]
        
        list.append(Req.getdate(start[num]))
        list.append(Req.dayinweek(Req.strdatetodt(Req.getdate(start[num]))))
        list.append(Req.gethourminute(start[num]))
        list.append(Req.gethourminute(lunch1[num]))
        list.append(Req.gethourminute(lunch2[num]))
        list.append(Req.gethourminute(end[num]))
        total = Req.find_workinghours(start[num],end[num])
        lunch = Req.find_workinghours(lunch1[num],lunch2[num])
        list.append(total-lunch)
        return list
    
    def findwh(num, start, lunch1, lunch2, end):
        total = Req.find_workinghours(start[num],end[num])
        lunch = Req.find_workinghours(lunch1[num],lunch2[num])
        return total - lunch
    
    def findremainder(desiredhours, weeklyhourlimit, hoursinweek):
        list = []
        remainder = desiredhours % weeklyhourlimit
        if remainder>8:
            list.append(8)
            list.append(remainder-8)
            Temp.leftover = remainder-8
            return list
        else: 
            list.append(remainder)
            Temp.leftover = remainder
            list.append(0)
            return list
    
    def main():
        working_hours1 = 0
        within = False
        count = 0
        datediff = Req.listdatediff(Temp.startdate, Temp.enddate)  
        weeks = Req.calcweeks(int(datediff))

        if weeks * 15 < ReadExcel.desired_work_hours_limit():
            sg.Popup('The entered desired hours exceeds the FEO hours limit. The desired hours should be under: ' + str(int(weeks * 15)) + ' hours')
            quit()

        list = []
        list.append(Temp.findwh(count, Temp.genstart1d1, Temp.genlunch1d1, Temp.genlunch2d1, Temp.genendd1))
        list.append(Temp.findwh(count, Temp.genstart1d2, Temp.genlunch1d2, Temp.genlunch2d2, Temp.genendd2))

        while (within == False):
            if working_hours1 + list[0] > ReadExcel.desired_work_hours_limit():
                within = True
                Temp.working_hours.append(Temp.findremainder(ReadExcel.desired_work_hours_limit(), ReadExcel.total_weekly_hour_limit(), 0))
                break

            if working_hours1 + list[0] <= ReadExcel.desired_work_hours_limit():
                list1 = Temp.compile(count, Temp.genstart1d1, Temp.genlunch1d1, Temp.genlunch2d1, Temp.genendd1)
                list1.append(ReadExcel.get_duty())
                Temp.dates.append(list1)
                working_hours1 = working_hours1 + list[0]

            if working_hours1 + list[1] > ReadExcel.desired_work_hours_limit():
                within = True
                Temp.working_hours.append(Temp.findremainder(ReadExcel.desired_work_hours_limit(), ReadExcel.total_weekly_hour_limit(), 8))
                break

            if working_hours1 + list[1] <= ReadExcel.desired_work_hours_limit():
                list1 = Temp.compile(count, Temp.genstart1d2, Temp.genlunch1d2, Temp.genlunch2d2, Temp.genendd2)
                list1.append(ReadExcel.get_duty())
                Temp.dates.append(list1)
                working_hours1 = working_hours1 + list[1]

            else:
                within = True

            count = count + 1
            Temp.working_hours.append(list)

        #validate weekly
        for num in range(0, len(Temp.working_hours)):
            if Req.validateweeklyhours(Temp.working_hours[num][0] + Temp.working_hours[num][1]) == False:
                quit()
        
        #validate total
        tally = 0
        for num2 in range(0, len(Temp.working_hours)):
            tally = tally + Temp.working_hours[num2][0] + Temp.working_hours[num2][1]
        if Req.validateworkinghours(tally) ==  False:
            quit()

        tally2 = tally
        #validate date range
        if Req.validatedatediff(Req.listdatediff(Temp.startdate, Temp.enddate)) == False:
            quit()

        lastday = Temp.days[-1]
        lastdaycount = -1
        if  0 < Temp.leftover < 2:
            if Req.dayinweek(Req.strdatetodt(lastday)) == "Sunday":
                    lastday = Temp.days[-2]
                    lastdaycount = -2

            taken = 2 - Temp.leftover        

            secondlasthour = Temp.dates[lastdaycount][6] * 60
            secondleftlasthour = secondlasthour - taken*60
            Temp.dates[lastdaycount][6] = secondleftlasthour/60

            lefthour = int(Temp.leftover)
            leftovermin = Temp.leftover * 60 - lefthour * 60
            secondlastend = Temp.dates[lastdaycount][5]
            timetoremove = taken * 60
            dttime = dt.datetime.strptime(secondlastend,"%H:%M:%S")
            result = dttime - dt.timedelta(minutes = timetoremove)
            result = str(result).split(' ')
            Temp.dates[-1][5] = result[1]
            lastdaylist = [lastday,Req.dayinweek(Req.strdatetodt(lastday)),Req.timetostr(9, 0), "N/A", "N/A", Req.timetostr(11,0), 2, ReadExcel.get_duty()]
            Temp.dates.append(lastdaylist)



        if Temp.leftover >= 2:
            lastday = Temp.days[-1]
            lefthour = int(Temp.leftover)
            leftovermin = Temp.leftover * 60 - lefthour * 60
            if Req.dayinweek(Req.strdatetodt(lastday)) == "Sunday":
                    lastday = Temp.days[-2]
            if Temp.leftover <= 4:
                lastdaylist = [lastday,Req.dayinweek(Req.strdatetodt(lastday)),Req.timetostr(9, 0), "N/A", "N/A", Req.timetostr(9 + lefthour, leftovermin), Temp.leftover, ReadExcel.get_duty()]
                Temp.dates.append(lastdaylist)
            if weeks*15 < ReadExcel.desired_work_hours_limit()-8:
                sg.Popup('The entered desired hours exceeds the FEO hours limit. The desired hours should be under: ' + str(int(weeks * 15)) + ' hours')
                quit()
            if Temp.leftover > 4:
                lastdaylist = [lastday,Req.dayinweek(Req.strdatetodt(lastday)),Req.timetostr(9, 0), "13:00:00", "14:00:00", Req.timetostr(9 + lefthour + 1, leftovermin), Temp.leftover, ReadExcel.get_duty()]
                Temp.dates.append(lastdaylist)

        for x in range(0, len(Temp.dates)):
            Temp.gd.loc[len(Temp.gd)] = Temp.dates[x]  

        gd2data = [weeks, datediff, tally, int(weeks*15)]

        Temp.gd4.columns = [''] * len(Temp.gd4.columns)
        Temp.gd4.loc[len(Temp.gd4)] = tally 

        exceledit.EditExcel.specinsert2(Temp.gd4,'Results', False, False, 6, 17)
        Temp.gd2.loc[len(Temp.gd2)] = gd2data
        exceledit.EditExcel.specinsert(Temp.gd2,'Results', False, 9, 0)
        exceledit.EditExcel.specinsert(Temp.gd,'Results', False, 0, 0)
        exceledit.EditExcel.specinsert(Temp.gd3,'Results',False, 5, 17)
        exceledit.EditExcel.setupresult()
        exceledit.EditExcel.writer.save()
        os.startfile('result.xlsx')

Temp.main()