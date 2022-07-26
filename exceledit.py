from operator import index
import pandas as pd
from openpyxl import load_workbook
import datetime as dt
import numpy
import PySimpleGUI as sg
import socket


class EditExcel():
    writer = pd.ExcelWriter("test.xlsx", engine='xlsxwriter')

    def insert(dataframe,tab_name):
        dataframe.to_excel(EditExcel.writer, sheet_name=tab_name)

    def specinsert(dataframe,tab_name,tf,sc,sr):
        dataframe.to_excel(EditExcel.writer, sheet_name=tab_name, index = tf, startcol = sc, startrow = sr)
        
    def replace(dataframe, col, old, val):
        dataframe[col] = dataframe[col].replace([old],[val])

    def test():
        EditExcel.insert(EditExcel.df3,'tab')
        EditExcel.specinsert(EditExcel.df2,'tab', False, 1, 5)
        EditExcel.writer.save()

