import exceledit 
import pandas as pd
import datetime as dt
import numpy
from excelreader import ReadExcel
from calculation import Req
import glob

class Temp():

    startdate = ReadExcel.find_start()
    enddate = ReadExcel.find_end()
    
    dayofweek1 = ReadExcel.dayofweek1()
    dayofweek2 = ReadExcel.dayofweek2()


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

    ddf1 = pd.DataFrame({
                'Total Days': [Req.datediff(starttime, endtime)],
                'Total Hours': [0]}
                )
    ddf2 = pd.DataFrame({'Start Date': [startdate[0], startdate[1], startdate[2]], 
                'End Date': [enddate[0], enddate[1], enddate[2]]},
                index=['Year', 'Month', 'Day'] 
                )
    
    gd = pd.DataFrame(
                columns = ['Date','Day','Office Start', 'Lunch Start', 'Lunch End', 'Office End','Working Hours']
                )
    
    gd2 = pd.DataFrame(index =  ['Date and Time'])
    
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
    

    def main():
        #exceledit.EditExcel.replace(Temp.ddf1, 'Total Days', 0, 100)
        #exceledit.EditExcel.insert(Temp.ddf2,'Tab')
        #exceledit.EditExcel.specinsert(Temp.ddf1,'Tab', False, 1, 5)
        #for x in range(len(Temp.dates)):
            #Temp.gd2.loc[len(Temp.gd2)] = Temp.dates[x]
        #exceledit.EditExcel.specinsert(Temp.gd2,'Tab', False, 5, 0)
        #print (Temp.genstart1d1)
        for x in range(len(Temp.genstart1d1) - 1):
            Temp.compile(x, Temp.genstart1d1, Temp.genlunch1d1, Temp.genlunch2d1, Temp.genendd1)
            Temp.compile(x, Temp.genstart1d2, Temp.genlunch1d2, Temp.genlunch2d2, Temp.genendd2)

        for x in range(len(Temp.dates)):
            Temp.gd.loc[len(Temp.gd)] = Temp.dates[x]
        #print (Temp.dates)
        #print(Temp.dates)

        #print(Temp.dates[0][6])

        exceledit.EditExcel.specinsert(Temp.gd,'Tab', False, 0, 0)
        exceledit.EditExcel.writer.save() 
        #Temp.comp_gendates(Temp.genstart, Temp.genlunch1, Temp.genlunch2, Temp.genend)
        return
 
Temp.main()

#print (Temp.genstart1d1)
