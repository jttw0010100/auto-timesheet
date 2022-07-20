from operator import index
import pandas as pd
from openpyxl import load_workbook
from calculation import Req
import datetime as dt
import numpy

class EditExcel():
    writer = pd.ExcelWriter("test.xlsx", engine='xlsxwriter')

    def insert(dataframe,tab_name):
        dataframe.to_excel(EditExcel.writer, sheet_name=tab_name)

    def specinsert(dataframe,tab_name,tf,sc,sr):
        dataframe.to_excel(EditExcel.writer, sheet_name=tab_name, index = tf, startcol = sc, startrow = sr)
        
    def replace(dataframe, col, old, val):
        dataframe[col] = dataframe[col].replace([old],[val])

    def test():
        EditExcel.replace(EditExcel.df2, 'Total Days', 0, 100)
        EditExcel.insert(EditExcel.df3,'tab')
        EditExcel.specinsert(EditExcel.df2,'tab', False, 1, 5)
        EditExcel.writer.save()

    def generate(startdate, enddate, dayinweek):
        
        periods = pd.date_range(start=startdate, end = enddate, freq="7D", inclusive="both")
        print (numpy.array(periods))
