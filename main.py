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
    starttime = Req.addtimetodate(ReadExcel.find_start(), 9,0)
    lunchstart = Req.addtimetodate(ReadExcel.find_start(), 13,0)
    lunchend = Req.addtimetodate(ReadExcel.find_start(), 14,0)
    endtime = Req.addtimetodate(ReadExcel.find_start(),18,0)
    datelist = []
    genstart = Req.generate(Req.findday(starttime,"Mon"), enddate,"7D")
    genstart2 = Req.generate(Req.findday(starttime,"Mon"), enddate,"14D")
    genlunch1 = Req.generate(Req.findday(lunchstart,"Mon"), enddate, "7D")
    genlunch2 = Req.generate(Req.findday(lunchend,"Mon"), enddate, "7D")
    genend = Req.generate(Req.findday(endtime,"Mon"), enddate, "7D")
    numofdates = len(genstart) + len(genlunch1) + len(genlunch2) + len(genend)
    genstart3 = []
    dates = []
    hours = [8,7]

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
    
    #compile dates
    #for x in range(int(numofdates/4)):
        #dates.append(genstart3[x])
        #dates.append(genlunch1[x])
        #dates.append(genlunch2[x])
        #dates.append(genend[x])

    def compile(num):
        list=[]
        list.append(Req.getdate(Temp.genstart[num]))
        list.append(Req.dayinweek(Req.strdatetodt(Req.getdate(Temp.genstart[num]))))
        list.append(Req.gethourminute(Temp.genstart[num]))
        list.append(Req.gethourminute(Temp.genlunch1[num]))
        list.append(Req.gethourminute(Temp.genlunch2[num]))
        list.append(Req.gethourminute(Temp.genend[num]))
        total = Req.find_workinghours(Temp.genstart[num],Temp.genend[num])
        lunch = Req.find_workinghours(Temp.genlunch1[num],Temp.genlunch2[num])
        list.append(total-lunch)
        print (list)
    

    def main():
        #exceledit.EditExcel.replace(Temp.ddf1, 'Total Days', 0, 100)
        #exceledit.EditExcel.insert(Temp.ddf2,'Tab')
        #exceledit.EditExcel.specinsert(Temp.ddf1,'Tab', False, 1, 5)
        #for x in range(len(Temp.dates)):
            #Temp.gd2.loc[len(Temp.gd2)] = Temp.dates[x]
        #exceledit.EditExcel.specinsert(Temp.gd2,'Tab', False, 5, 0)
        """
        for x in range(10):
            x1 = x%2
            Temp.gd.loc[len(Temp.gd)] = Temp.dates[x1]
        """
        Temp.compile(0)
        #print(Temp.dates)
        #exceledit.EditExcel.specinsert(Temp.gd,'Tab', False, 4, 0)
        #exceledit.EditExcel.writer.save() 
        #Temp.comp_gendates(Temp.genstart, Temp.genlunch1, Temp.genlunch2, Temp.genend)
        return
 
Temp.main()
