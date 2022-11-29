import time
import digitalio
import board
import busio
import adafruit_hcsr04
import adafruit_bmp280

import csv

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x76)

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D4, echo_pin=board.D17)

led = digitalio.DigitalInOut(board.D18)
led.direction = digitalio.Direction.OUTPUT

print("--- Proyecto 3 ---")
num = int(input("Numero de muestras: "))
freq = float(input("Frecuencia de muestreo: "))

data = []
data.append(["temperature", "distance"])



temperature =  round(sensor.temperature, 2)
print("Temperatura ambiente: "+ str(temperature))

print("Comenzando toma de datos en...")
print("3")
time.sleep(1)
print("2")
time.sleep(1)
print("1")
time.sleep(1)

for i in range(num):
    led.value = True
    temperature =  round(sensor.temperature, 2)
    distance = round(sonar.distance, 2)
    print("["+str(i+1)+"](distancia=" + str(distance) + ", temperatura=" + str(temperature) + ")")  
    data.append([temperature, distance])    
    led.value = False 
    time.sleep(freq)

with open('data.csv', mode='w') as data_file:
    data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for item in data:
      data_writer.writerow(item)
      
      
gauth = GoogleAuth()
# Try to load saved client credentials
gauth.LoadCredentialsFile("mycreds.txt")
if gauth.credentials is None:
    # Authenticate if they're not there
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    # Refresh them if expired
    gauth.Refresh()
else:
    # Initialize the saved creds
    gauth.Authorize()
# Save the current credentials to a file
gauth.SaveCredentialsFile("mycreds.txt")

drive = GoogleDrive(gauth)

textfile = drive.CreateFile({'id' : '152GVaaZm2ocJ-IJsUQE1gqqXu7jPWRN6'})
textfile.SetContentFile('data.csv')
textfile.Upload()
print("\nUploaded successfully!")