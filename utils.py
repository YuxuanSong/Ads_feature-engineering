import time
import datetime

def Checkline(obj):
    if len(obj)==30 and len(obj['device'])==15:
        return 0
    else:
        return 1


def time_modifier(timestring,timezone):    #get the current weekday and hour
    timeArray = time.strptime(timestring,"%Y-%m-%d %H:%M:%S UTC")
    timeStamp = int(time.mktime(timeArray))
    TimeRes = int(timezone)*60
    Localtime = timeStamp + TimeRes
    Modifier = datetime.datetime.fromtimestamp(Localtime)
    weekday = Modifier.weekday()
    hour = Modifier.hour
    return str(weekday+1), str(hour)


def device_brand(price):
    if price == 'Unknown':
        return  'Unknown'
    price = int(price)
    if price<=500:
        return '-500'
    elif price<=1000:
        return '500-1000'
    elif price <=1500:
        return '1000-1500'
    elif price<=2000:
        return '1500-2000'
    elif price <=2500:
        return '2000-2500'
    else:
        return '2500+'


def FeatureTrans(field,content,timezone=' '):
    if field == ' rice':
        return device_brand(content)

    if field == 'timestamp':
        return time_modifier(content,timezone)





#print  time_modifier("2017-02-22 23:49:40 UTC",'-210')





