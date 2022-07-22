import exceledit 
import pandas as pd
import datetime as dt
import numpy
from excelreader import ReadExcel
from calculation import Req


class Temp():
    startdate = ReadExcel.find_start()
    enddate = ReadExcel.find_end()
    starttime = Req.addtimetodate(ReadExcel.find_start(), 9,0)
    lunchstart = Req.addtimetodate(ReadExcel.find_start(), 13,0)
    lunchend = Req.addtimetodate(ReadExcel.find_start(), 14,0)
    endtime = Req.addtimetodate(ReadExcel.find_start(),18,0)
    datelist = []
    genstart = Req.generate(Req.findday(starttime,"Sun"), enddate,"7D")
    #genstart2 = Req.generate(Req.findday(starttime,"Sun"), enddate,"14D")
    genlunch1 = Req.generate(Req.findday(lunchstart,"Sun"), enddate, "7D")
    genlunch2 = Req.generate(Req.findday(lunchend,"Sun"), enddate, "7D")
    genend = Req.generate(Req.findday(endtime,"Sun"), enddate, "7D")
    numofdates = len(genstart) + len(genlunch1) + len(genlunch2) + len(genend)
    #genstart3 = []
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
    
    #compile dates
    for x in range(int(numofdates/4)):
        dates.append(genstart[x])
        dates.append(genlunch1[x])
        dates.append(genlunch2[x])
        dates.append(genend[x])

    def main():
        #exceledit.EditExcel.replace(Temp.ddf1, 'Total Days', 0, 100)
        #exceledit.EditExcel.insert(Temp.ddf2,'Tab')
        #exceledit.EditExcel.specinsert(Temp.ddf1,'Tab', False, 1, 5)
        #for x in range(len(Temp.dates)):
            #Temp.gd2.loc[len(Temp.gd2)] = Temp.dates[x]
        #exceledit.EditExcel.specinsert(Temp.gd2,'Tab', False, 5, 0)
        exceledit.EditExcel.specinsert(Temp.gd,'Tab', True, 4, 0)
        exceledit.EditExcel.writer.save() 
        #Temp.comp_gendates(Temp.genstart, Temp.genlunch1, Temp.genlunch2, Temp.genend)
        return
 

Temp.main()
