import pandas as pd
import openpyxl
import xlrd
from calculation import Req

loc = ("datainput.xls")
 
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)

class ReadExcel():
    Statutory_Holidays = ['2022-01-01','2022-02-01','2022-02-02','2022-02-03','2022-04-05','2022-05-01','2022-05-08','2022-06-03','2022-07-01','2022-09-12','2022-10-01','2022-10-04','2022-12-22','2022-12-25'] 
    Start_date = 0
    End_date = 0

    def get_value(sheetnum, row, column):
        sheet = wb.sheet_by_index(sheetnum)
        return sheet.cell_value(row, column)

    def compile_dates(sheetnum, yearrow, monthrow, dayrow):
        sheet = wb.sheet_by_index(sheetnum)
        year = sheet.cell_value(yearrow, 1)
        month = sheet.cell_value(monthrow, 1)
        day =  sheet.cell_value(dayrow, 1)
        return Req.datecomp(year, month, day)

    def find_start():
        return ReadExcel.compile_dates(0, 1, 2, 3)
    
    def find_end():
        return ReadExcel.compile_dates(0, 7, 8, 9)
    
    def total_hour_limit():
        return ReadExcel.get_value(0, 12, 1)

    def total_date_range_limit():
        return ReadExcel.get_value(0, 13, 1)

    def total_work_hour_limit():
        return ReadExcel.get_value(0, 14, 1)

    def office_start():
        return ReadExcel.get_value(0, 15, 1)

    def lunch_start():
        return ReadExcel.get_value(0, 16, 1)

    def lunch_end():
        return ReadExcel.get_value(0, 17, 1)
    
    def office_end():
        return ReadExcel.get_value(0, 18, 1)

    