import math
import time , datetime

##################################################################################################################
def date2mjd(year,month,day,hour,minute,second):

    if month == 1 or month == 2:
        yearp = year - 1
        monthp = month + 12
    else:
        yearp = year
        monthp = month
    
    # this checks where we are in relation to October 15, 1582, the beginning
    # of the Gregorian calendar.
    if ((year < 1582) or
        (year == 1582 and month < 10) or
        (year == 1582 and month == 10 and day < 15)):
        # before start of Gregorian calendar
        B = 0
    else:
        # after start of Gregorian calendar
        A = math.trunc(yearp / 100.)
        B = 2 - A + math.trunc(A / 4.)
        
    if yearp < 0:
        C = math.trunc((365.25 * yearp) - 0.75)
    else:
        C = math.trunc(365.25 * yearp)
        
    D = math.trunc(30.6001 * (monthp + 1))
    
    jd = B + C + D + day + 1720994.5
    mjd = jd - 2400000.5 + hour/24. + minute/1440. + second/86400.
    return mjd
#############################################################################################################################
#def date2mjd(year,month,day,hour,minute,second):
#a = math.trunc((14-month)/12)
#y = year + 4800 - a
#mjd = (day +  math.trunc((153*(month+12*a-3)+2)/5) + math.trunc(365*y) + math.trunc(y/4) - math.trunc(y/100) + math.trunc(y/400) - 2432046
#       + hour/24. + minute/1440. + second/86400.)
    
################################################################################################################
#def date2mjd(year,month,day,hour,minute,second):
#    year=1859;month=9;day=2;hour=0;minute=0;second=0;
#    y = year - 1859
#    yd = math.trunc(y*365.25)                       # 1 year = 365.25 days
#    md = math.trunc((month-1)*30.4368)       # 1 month = 30.4368 days
#    mjd = yd + 44 + md + day + math.trunc(hour/24) + math.trunc(minute/1440) + math.trunc(second/86400)     #   44 is number of days from 17 nov to 31 dec
#    return mjd    
#######################################################################################################################       
def mjd2date(mjd):
    f,i = math.modf(mjd)
    jd = i + 2400000.5 
    jd = jd + 0.5
    
    F, I = math.modf(jd)
    I = int(I)
    
    A = math.trunc((I - 1867216.25)/36524.25)
    
    if I > 2299160:
        B = I + 1 + A - math.trunc(A / 4.)
    else:
        B = I
        
    C = B + 1524
    
    D = math.trunc((C - 122.1) / 365.25)
    
    E = math.trunc(365.25 * D)
    
    G = math.trunc((C - E) / 30.6001)
    
    day = C - E + F - math.trunc(30.6001 * G)
    
    if G < 13.5:
        month = G - 1
    else:
        month = G - 13
        
    if month > 2.5:
        year = D - 4716
    else:
        year = D - 4715
        
    hours = f * 24.
    hours, hour = math.modf(hours)
    
    mins = hours * 60.
    mins, minute = math.modf(mins)
    
    secs = mins * 60.
    secs, second = math.modf(secs)
      
    return year, month, day ,hour, minute, second
########################################################################################################################   
    
def time2sec(hour,minute,second):
    sec = hour*3600 + minute*60 + second
    return sec    
############################################################################################################################ 

def sec2time(second):
    hour_frac, hour = math.modf(second/3600)
    min_frac, minute_total = math.modf(hour_frac*3600)
    minute_frac, minute = math.modf(minute_total/60)
    second = round(minute_frac * 60)
    return int(hour), int(minute), int(second)
###############################################################################

def date2WN(year, month, day, hour, minu, sec):
    """converts UTC to: gpsWeek, secsOfWeek, gpsDay, secsOfDay 95 96 
    a good reference is: http://www.oc.nps.navy.mil/~jclynch/timsys.html 97 98 
    This is based on the following facts (see reference above): 99 100 
    GPS time is basically measured in (atomic) seconds since 101 
    January 6, 1980, 00:00:00.0 (the GPS Epoch) 102 103 
    The GPS week starts on Saturday midnight (Sunday morning), and runs 104 
    for 604800 seconds. 105 106 
    Currently, GPS time is 13 seconds ahead of UTC (see above reference). 107 
    While GPS SVs transmit this difference and the date when another leap 108 
    second takes effect, the use of leap seconds cannot be predicted. This 109 
    routine is precise until the next leap second is introduced and has to be 110 
    updated after that. 111 112 
    SOW = Seconds of Week 113 
    SOD = Seconds of Day 114 115 N
    ote: Python represents time in integer seconds, fractions are lost!!! 116 
    """  

    secsInWeek = 604800   #  number of sec in a week
    secsInDay = 86400
    gpsEpoch = (1980, 1,6, 0, 0, 0)  # gps epoch for gps week number(6 jan,1980) 
    secFract = sec % 1 
    epochTuple = gpsEpoch + (-1, -1, 0) 
    t0 = time.mktime(epochTuple) 
    t = time.mktime((year, month, day, hour, minu, int(sec), -1, -1, 0)) 
    # Note: time.mktime strictly works in localtime and to yield UTC, it should be 122 
    # corrected with time.timezone 123 
    # However, since we use the difference, this correction is unnecessary. 124 
    # Warning: trouble if daylight savings flag is set to -1 or 1 !!! 125  
    tdiff = t - t0 
    gpsSOW = (tdiff % secsInWeek) + secFract 
    gpsWeek = int(math.floor(tdiff/secsInWeek)) 
    gpsDay = int(math.floor(gpsSOW/secsInDay)) 
    gpsSOD = (gpsSOW % secsInDay) 
    return (gpsWeek, gpsSOW, gpsDay, gpsSOD)
