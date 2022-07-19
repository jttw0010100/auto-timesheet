import datetime as dt

class Req():
    #max weekly hours
    maxwh=15
    #max total hours
    maxth=126
    #max date range
    maxdr = 59

    def calcwh(start, lunchs, lunche, finish):
        if finish-start+1>15:
            return False
        else:
            return True

class Datetime(Req):

    def convert(time):
        timelist = []
        timelist = time.split(':')
        return timelist

print(Datetime.convert("04:01"))