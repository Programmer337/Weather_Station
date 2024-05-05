import smbus2
import bme280
import MySQLdb
import requests
import json

port = 1
address = 0x77
bus = smbus2.SMBus(port)

calibration_params = bme280.load_calibration_params(bus, address)


data = bme280.sample(bus, address, calibration_params)
db = MySQLdb.connect('localhost','weather_station', 'MeineWetterstation1',  'weather_station')
cursor = db.cursor()

query = "INSERT INTO inside(time, temperature, pressure, humidity) VALUES (CURRENT_TIMESTAMP, " + str(data.temperature) + ", " + str(data.pressure) + ", " + str(data.humidity) + ");"
print(query)
print (cursor.execute(query))
db.commit()

res = requests.get("http://Aussenstation-ESP32.fritz.box")
if(res.status_code == 200):
    json = res.json()
    temperature = json["temperature"]
    pressure = json["pressure"]
    humidity = json["humidity"]
    query = "INSERT INTO outside(time, temperature, pressure, humidity) VALUES (CURRENT_TIMESTAMP, " + str(temperature) + ", " + str(pressure) + ", " + str(humidity) + ");"
    print(query)
    print (cursor.execute(query))
    db.commit()
else:
    print (res.status_code)

db.close()
print("Ende")