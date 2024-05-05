import matplotlib.pyplot as plt
import matplotlib.dates as plotDates
import MySQLdb
import datetime
from dateutil.relativedelta import relativedelta
import sys
import os

wd = os.getcwd()
print(wd)
if (wd == "/var/www/html/innen"):
    table = "inside"
if (wd=="/var/www/html/aussen"):
    table = "outside"

last = 0
period = 0
if (len(sys.argv) == 2):
    mode = "last"
    last = sys.argv[1]
elif(len(sys.argv) == 3):
    mode = "period"
    period = sys.argv[1]
    date = sys.argv[2]

db = MySQLdb.connect('localhost','weather_station', 'MeineWetterstation1',  'weather_station')
cursor = db.cursor()

if(mode == "last"):
    query = "SELECT * FROM "+table+" WHERE time > "
    if (last == "last24"):
        query += "subdate(CURRENT_TIMESTAMP, interval 1 day);"
    elif(last == "week"):
        query += "subdate(CURRENT_TIMESTAMP, interval 1 week);"
    elif(last == "month"):
        query += "subdate(CURRENT_TIMESTAMP, interval 1 month);"
    elif(last == "year"):
        query += "subdate(CURRENT_TIMESTAMP, interval 1 year);"
elif(mode == "period"):
    if (period == "day"):
        query = "SELECT * FROM "+table+" WHERE time >= DATE('"+date+"') AND time < DATE('"+str(datetime.datetime.strptime(date, "%Y-%m-%d") + datetime.timedelta(days=1))+"');"
    elif(period == "month"):
        query = "SELECT * FROM "+table+" WHERE time >= DATE('"+date+"-00') AND time < DATE('"+str(datetime.datetime.strptime(date, "%Y-%m") + relativedelta(months=+1))+"');"
    elif(period == "year"):
        query = "SELECT * FROM "+table+" WHERE time >= DATE('"+date+"-00-00') AND time < DATE('"+str(int(date)+1)+"-00-00 00:00:00');"

cursor.execute (query)
result = cursor.fetchall()
db.close()

resLen = len(result)
x=[]
temp=[]
pressure=[]
hum=[]
for i in range(0, resLen): # put values in the variables
    x.append((result[i][0]))
for i in range(0, resLen):
    temp.append(result[i][1])
for i in range(0, resLen):
    pressure.append(result[i][2])
for i in range(0, resLen):
    hum.append(result[i][3])

fig, axs = plt.subplots(3)
for i in range(0,3):
    axs[i].xaxis_date()
    if(last == "last24" or period == "day"):
        axs[i].xaxis.set_major_formatter(plotDates.DateFormatter("%H:%M")) # Variable
    elif(last == "week" or last=="month" or period == "month"):
        axs[i].xaxis.set_major_formatter(plotDates.DateFormatter("%d.%m"))
    elif(last == "year" or period == "year"):
        axs[i].xaxis.set_major_formatter(plotDates.DateFormatter("%m"))
fig.suptitle('Wetterstation')
axs[0].set_title('Temperatur')
axs[1].set_title('Luftdruck')
axs[2].set_title('Luftfeuchtigkeit')

axs[0].set(ylabel="°C")
axs[1].set(ylabel="hPa")
axs[2].set(ylabel="%")

axs[0].plot(x, temp, color="red")
axs[1].plot(x, pressure, color="green")
axs[2].plot(x, hum, color="blue")
fig.tight_layout()

if(mode == "last"):
    path = "pictures/" + last + ".svg"
else:
    path = "pictures/" + date + ".svg"

print(path)
plt.savefig(path)
#plt.show()