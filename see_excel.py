from calendar import day_abbr
import pandas as pd
import openpyxl
import xlrd

loc = ("datainput.xls")
 
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)

class ReadExcel():
    

    def get_value(sheetnum, row, column):
        sheet = wb.sheet_by_index(sheetnum)
        return sheet.cell_value(row, column)

    def datecomp(year, month, day):
        date = [year, month, day]
        return date

    def compile_dates(sheetnum, yearrow, monthrow, dayrow):
        sheet = wb.sheet_by_index(sheetnum)
        year = sheet.cell_value(yearrow, 1)
        month = sheet.cell_value(monthrow, 1)
        day =  sheet.cell_value(dayrow, 1)
        return ReadExcel.datecomp(int(year), int(month), int(day))

    def find_start():
        return ReadExcel.compile_dates(0, 1, 2, 3)
    
    def find_end():
        return ReadExcel.compile_dates(0, 6, 7, 8)
    
    def total_work_hours_limit():
        return ReadExcel.get_value(0, 11, 1)
    
    def desired_work_hours_limit():
        return ReadExcel.get_value(0, 12, 1)

    def total_date_range_limit():
        return ReadExcel.get_value(0, 13, 1)

    def total_weekly_hour_limit():
        return ReadExcel.get_value(0, 14, 1)

    def office_start():
        return ReadExcel.get_value(0, 15, 1)

    def lunch_start():
        return ReadExcel.get_value(0, 16, 1)

    def lunch_end():
        return ReadExcel.get_value(0, 17, 1)
    
    def office_end():
        return ReadExcel.get_value(0, 18, 1)

    def dayofweek1():
        return str(ReadExcel.get_value(0, 21, 1))
    
    def dayofweek2():
        return str(ReadExcel.get_value(0, 22, 1))
    
    def get_public_holidays():
        list = []
        for i in range(12):
            year = ReadExcel.get_value(1, 1, 1)
            month = ReadExcel.get_value(1, i+1, 2)
            day = ReadExcel.get_value(1, i+1, 3)
            year = int(year)
            year = str(year)
            month = int(month)
            if month<10:
                month = str(month)
                month = "0" + month
            else:
                month = str(month)
            day = int(day)
            if day<10:
                day = str(day)
                day = "0" + day
            else:
                day = str(day)
            date = year + "-" + month + "-" + day
            list.append(date)
        return (list)

