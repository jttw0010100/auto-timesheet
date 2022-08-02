from cgitb import text
from operator import index
import pandas as pd
import datetime as dt
import numpy
from openpyxl.styles import Border, Side
import PySimpleGUI as sg
import socket
import xlsxwriter

from see_excel import ReadExcel 

class EditExcel():
    writer = pd.ExcelWriter("result.xlsx", engine='xlsxwriter')
    workbook = xlsxwriter.Workbook("result.xlsx")
    worksheet1 = workbook.add_worksheet()


    def setupresult():
        EditExcel.writer.sheets['Results'].set_column(0,0, 15)
        EditExcel.writer.sheets['Results'].set_column(1,1, 10)
        EditExcel.writer.sheets['Results'].set_column(2,4, 10)
        EditExcel.writer.sheets['Results'].set_column(5,5, 15)
        EditExcel.writer.sheets['Results'].set_column(6,6, 7)
        EditExcel.writer.sheets['Results'].set_column(9,9, 10)
        EditExcel.writer.sheets['Results'].set_column(10,10, 9)
        EditExcel.writer.sheets['Results'].set_column(11,12, 13)

    def insert(dataframe,tab_name):
        dataframe.to_excel(EditExcel.writer, sheet_name=tab_name)

    def specinsert(dataframe,tab_name,tf,sc,sr):
        dataframe.to_excel(EditExcel.writer, sheet_name=tab_name, index = tf, startcol = sc, startrow = sr)
    
    def specinsert2(dataframe,tab_name,tf, head ,sc,sr):
        dataframe.to_excel(EditExcel.writer, sheet_name=tab_name, index = tf, header = head,startcol = sc, startrow = sr)
        
    def replace(dataframe, col, old, val):
        dataframe[col] = dataframe[col].replace([old],[val])

    


