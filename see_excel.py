from calendar import day_abbr
import pandas as pd
import openpyxl
import xlrd

df = pd.read_excel(r"datainput.xlsx",'Input')
df2 = pd.read_excel(r"datainput.xlsx",'Public Holidays')

class ReadExcel():

    def datecomp(year, month, day):
        date = [year, month, day]
        return date

    def find_start():
        return ReadExcel.datecomp(df.at[0, 'Unnamed: 1'], df.at[1, 'Unnamed: 1'], df.at[2, 'Unnamed: 1'])
    
    def find_end():
        return ReadExcel.datecomp(df.at[5, 'Unnamed: 1'], df.at[6, 'Unnamed: 1'], df.at[7, 'Unnamed: 1'])
    
    def total_work_hours_limit():
        return df.at[10, 'Unnamed: 1']
    
    def desired_work_hours_limit():
        return df.at[11, 'Unnamed: 1']

    def total_date_range_limit():
        return df.at[12, 'Unnamed: 1']

    def total_weekly_hour_limit():
        return df.at[13, 'Unnamed: 1']

    def office_start():
        return df.at[14, 'Unnamed: 1']

    def lunch_start():
        return df.at[15, 'Unnamed: 1']

    def lunch_end():
        return df.at[16, 'Unnamed: 1']
    
    def office_end():
        return df.at[17, 'Unnamed: 1']

    def dayofweek1():
        return str(df.at[20, 'Unnamed: 1'])
    
    def dayofweek2():
        return str(df.at[21, 'Unnamed: 1'])
    
    def get_public_holidays():
        list = []
        for i in range(12):
            year = df2.at[i, 'Year']
            month = df2.at[i, 'Month']
            day = df2.at[i, 'Day']
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

    def get_duty():
        return str(df.at[23, 'Unnamed: 1'])