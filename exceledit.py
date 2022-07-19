from operator import index
import pandas as pd
from openpyxl import load_workbook


class EditExcel():
    writer = pd.ExcelWriter("test.xlsx", engine='xlsxwriter')

    df2 = pd.DataFrame({
                'Total Days': [1]},
                )

    df3 = pd.DataFrame({'Start Date': [0, 0, 0], 
                'End Date': [0, 0, 0]},
                index=['Year', 'Month', 'Day'] 
                )

    def insert(df,tab_name):
        df.to_excel(EditExcel.writer, sheet_name=tab_name)

    def specinsert(df,tab_name,tf,sc,sr):
        df.to_excel(EditExcel.writer, sheet_name=tab_name, index = tf, startcol = sc, startrow = sr)
        
    def replace(df, col, val):
        df[col] = df[col].replace([0],[val])

    def test():
        EditExcel.insert(EditExcel.df3,'tab')
        EditExcel.specinsert(EditExcel.df2,'tab', False, 1, 5)
        EditExcel.writer.save()

EditExcel.test()