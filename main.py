import exceledit 
import pandas as pd
import datetime as dt
import numpy
from excelreader import ReadExcel
from calculation import Req


class Temp():
    start = ReadExcel.find_start()
    end = ReadExcel.find_end()
    starttime = Req.addtimetodate(ReadExcel.find_start(), 9,0)
    endtime = Req.addtimetodate(ReadExcel.find_end(),9,0)
    gend1 = Req.generate(Req.findday(starttime,"Sun"), endtime)
    ddf1 = pd.DataFrame({
                'Total Days': [Req.datediff(starttime, endtime)],
                'Total Hours': [0]}
                )
    ddf2 = pd.DataFrame({'Start Date': [start[0], start[1], start[2]], 
                'End Date': [end[0], end[1], end[2]]},
                index=['Year', 'Month', 'Day'] 
                )
    
    gd = pd.DataFrame({'Datetime': [gend1[0], gend1[1], gend1[2]], 
                'Day': [1, 2, 3],
                'Working Hours': [8, 7, 8]},
                )

    def test():
        exceledit.EditExcel.replace(Temp.ddf1, 'Total Days', 0, 100)
        exceledit.EditExcel.insert(Temp.ddf2,'Tab')
        exceledit.EditExcel.specinsert(Temp.ddf1,'Tab', False, 1, 5)
        exceledit.EditExcel.specinsert(Temp.gd,'Tab', False, 4, 0)
        exceledit.EditExcel.writer.save() 

Temp.test()