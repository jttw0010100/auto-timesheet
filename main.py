import exceledit 
import pandas as pd

class Temp():
    ddf1 = pd.DataFrame({
                'Total Days': [0]},
                )

    ddf2 = pd.DataFrame({'Start Date': [0, 0, 0], 
                'End Date': [0, 0, 0]},
                index=['Year', 'Month', 'Day'] 
                )
    def test():
        exceledit.EditExcel.replace(Temp.ddf1, 'Total Days', 0, 100)
        exceledit.EditExcel.insert(Temp.ddf2,'tab')
        exceledit.EditExcel.specinsert(Temp.ddf1,'tab', False, 1, 5)
        exceledit.EditExcel.writer.save()

Temp.test()