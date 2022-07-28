import exceledit 
import pandas as pd
import datetime as dt
import numpy
from see_excel import ReadExcel
from calculation import Req
import PySimpleGUI as sg
import socket
import glob

class Temp():
    
    Statutory_Holidays = ReadExcel.get_public_holidays()
    Days_in_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    startdate = ReadExcel.find_start()
    enddate = ReadExcel.find_end()

    if Req.validatedate(Req.listtostrdate(startdate)) == False:
        sg.Popup('Oops!', 'Entered date start date ' + Req.listtostrdate(startdate) + 'does not exist')

    if Req.validatedate(Req.listtostrdate(enddate)) == False:
        sg.Popup('Oops!', 'Entered date end date ' + Req.listtostrdate(enddate) + ' does not exist')   
     
    days = []
    days = Req.generate2(Req.datelisttostr(startdate), enddate, "1D")

    dayofweek1 = ReadExcel.dayofweek1()
    dayofweek2 = ReadExcel.dayofweek2()

    blacklist = []

    invalid = 0
    for day in days:
        for holiday in Statutory_Holidays:
            if day == holiday:
                invalid = 0
                dayofweek = Req.dayinweek(Req.strdatetodt(day))
                if (dayofweek in Days_in_week):
                    Days_in_week.remove(dayofweek)
                    blacklist.append(dayofweek)
                if dayofweek1 == dayofweek or dayofweek2 == dayofweek:
                    invalid = invalid + 1
    
    if len(blacklist)>0:
        if dayofweek1 != blacklist[0] and dayofweek2 != blacklist[0]:
            if len(blacklist)>1:
                if dayofweek1 != blacklist[1] and dayofweek2 != blacklist[1]:
                    invalid = 0
            if len(blacklist)<=1:
                invalid = 0
    
    if invalid > 0:
        sg.Popup('The days in week you have chosen land on a public holiday. Please choose days from this list:', Days_in_week)
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
                columns = ['Date','Day','Office Start', 'Lunch Start', 'Lunch End', 'Office End','Hours']
                )
    
    gd2 = pd.DataFrame(
        columns = ['Weeks', 'Date Range', 'Total Hours', 'FEO limit hours']
        )
    #enddate - startdate/7 * 15

    #compile dates(not needed)
    #for x in range(int(numofdates/4)):
        #dates.append(genstart3[x])
        #dates.append(genlunch1[x])
        #dates.append(genlunch2[x])
        #dates.append(genend[x])

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
        Temp.dates.append(list)
        Temp.temp.append(total - lunch)
    

    def main():

        for x in range(len(Temp.genstart1d1) - 1):
            Temp.compile(x, Temp.genstart1d1, Temp.genlunch1d1, Temp.genlunch2d1, Temp.genendd1)
            Temp.compile(x, Temp.genstart1d2, Temp.genlunch1d2, Temp.genlunch2d2, Temp.genendd2)
            list = []
            list.append(Temp.temp[0])
            list.append(Temp.temp[1])
            Temp.working_hours.append(Temp.temp)
            Temp.temp = []

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
        
        #validate date range
        if Req.validatedatediff(Req.listdatediff(Temp.startdate, Temp.enddate)) == False:
            quit()

        datediff = Req.listdatediff(Temp.startdate, Temp.enddate)  
        weeks = Req.calcweeks(int(datediff))

        if float(tally) < ReadExcel.desired_work_hours_limit():
            leftover = ReadExcel.desired_work_hours_limit() - tally
            lastday = Temp.days[-1]
            lefthour = int(leftover)
            leftovermin = lefthour * 60 - leftover * 60
            if leftover <= 4:
                lastdaylist = [lastday,Req.dayinweek(Req.strdatetodt(lastday)),Req.timetostr(9, 0), "N/A", "N/A", Req.timetostr(9 + lefthour, leftovermin), leftover]
                Temp.dates.append(lastdaylist)
            else:
                lastdaylist = [lastday,Req.dayinweek(Req.strdatetodt(lastday)),Req.timetostr(9, 0), "13:00:00", "14:00:00", Req.timetostr(9 + lefthour + 1, leftovermin), leftover]
                Temp.dates.append(lastdaylist)
            if weeks*15 + 8 < ReadExcel.desired_work_hours_limit():
                sg.Popup('Oops!', 'Desired hours is not valid within dates chosen.')
                quit()

        
        for x in range(0, len(Temp.dates)):
            Temp.gd.loc[len(Temp.gd)] = Temp.dates[x]  

        gd2data = [weeks, datediff, tally, ReadExcel.total_work_hours_limit()]
        
        Temp.gd2.loc[len(Temp.gd2)] = gd2data
        exceledit.EditExcel.specinsert(Temp.gd2,'Results', False, 8, 0)
        exceledit.EditExcel.specinsert(Temp.gd,'Results', False, 0, 0)
        exceledit.EditExcel.setupresult()
        exceledit.EditExcel.writer.save() 
 
Temp.main()